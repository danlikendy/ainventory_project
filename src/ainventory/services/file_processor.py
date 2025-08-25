import pandas as pd
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import json
from pathlib import Path

from ..database.models import Product, Category, Brand, Warehouse, InventoryItem, Sale, DataUpload
from ..database.connection import get_db_context
from ..config import settings

logger = logging.getLogger(__name__)

class FileProcessor:
    """Сервис для обработки загруженных файлов"""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls', '.csv']
        self.max_file_size = settings.max_file_size
    
    async def process_file(self, file_path: str, file_type: str, warehouse_id: Optional[int] = None) -> Dict[str, Any]:
        """Обработка загруженного файла"""
        try:
            # Проверяем формат файла
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in self.supported_formats:
                raise ValueError(f"Неподдерживаемый формат файла: {file_ext}")
            
            # Читаем файл
            df = await self._read_file(file_path)
            
            # Обрабатываем данные в зависимости от типа
            if file_type == "products":
                result = await self._process_products(df)
            elif file_type == "inventory":
                result = await self._process_inventory(df, warehouse_id)
            elif file_type == "sales":
                result = await self._process_sales(df, warehouse_id)
            else:
                raise ValueError(f"Неизвестный тип файла: {file_type}")
            
            # Обновляем статус загрузки
            await self._update_upload_status(file_path, "completed", result["records_processed"])
            
            return {
                "success": True,
                "message": f"Файл успешно обработан. Обработано записей: {result['records_processed']}",
                "records_processed": result["records_processed"],
                "errors": result.get("errors", []),
                "warnings": result.get("warnings", [])
            }
            
        except Exception as e:
            logger.error(f"Ошибка обработки файла {file_path}: {e}")
            await self._update_upload_status(file_path, "failed", 0, str(e))
            raise
    
    async def _read_file(self, file_path: str) -> pd.DataFrame:
        """Чтение файла в DataFrame"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                # Пробуем разные кодировки
                for encoding in ['utf-8', 'cp1251', 'latin1']:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError("Не удалось определить кодировку CSV файла")
            else:
                df = pd.read_excel(file_path, engine='openpyxl')
            
            # Очищаем данные
            df = self._clean_dataframe(df)
            return df
            
        except Exception as e:
            logger.error(f"Ошибка чтения файла {file_path}: {e}")
            raise
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Очистка и подготовка DataFrame"""
        # Убираем пустые строки и столбцы
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Приводим названия столбцов к нижнему регистру
        df.columns = df.columns.str.lower().str.strip()
        
        # Убираем лишние пробелы в строковых данных
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
        
        return df
    
    async def _process_products(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Обработка файла с продуктами"""
        records_processed = 0
        errors = []
        warnings = []
        
        with get_db_context() as db:
            for index, row in df.iterrows():
                try:
                    # Проверяем обязательные поля
                    if pd.isna(row.get('sku')) or pd.isna(row.get('name')):
                        errors.append(f"Строка {index + 1}: Отсутствуют обязательные поля SKU или название")
                        continue
                    
                    # Проверяем, существует ли уже продукт с таким SKU
                    existing_product = db.query(Product).filter(Product.sku == str(row['sku'])).first()
                    if existing_product:
                        warnings.append(f"Строка {index + 1}: Продукт с SKU {row['sku']} уже существует")
                        continue
                    
                    # Создаем или находим категорию
                    category_id = None
                    if not pd.isna(row.get('category')):
                        category = db.query(Category).filter(Category.name == str(row['category'])).first()
                        if not category:
                            category = Category(name=str(row['category']))
                            db.add(category)
                            db.flush()
                        category_id = category.id
                    
                    # Создаем или находим бренд
                    brand_id = None
                    if not pd.isna(row.get('brand')):
                        brand = db.query(Brand).filter(Brand.name == str(row['brand'])).first()
                        if not brand:
                            brand = Brand(name=str(row['brand']))
                            db.add(brand)
                            db.flush()
                        brand_id = brand.id
                    
                    # Создаем продукт
                    product = Product(
                        sku=str(row['sku']),
                        name=str(row['name']),
                        description=str(row.get('description', '')) if not pd.isna(row.get('description')) else None,
                        category_id=category_id,
                        brand_id=brand_id,
                        unit_cost=float(row['unit_cost']) if not pd.isna(row.get('unit_cost')) else None,
                        unit_price=float(row['unit_price']) if not pd.isna(row.get('unit_price')) else None,
                        weight=float(row['weight']) if not pd.isna(row.get('weight')) else None,
                        dimensions=str(row['dimensions']) if not pd.isna(row.get('dimensions')) else None
                    )
                    
                    db.add(product)
                    records_processed += 1
                    
                except Exception as e:
                    errors.append(f"Строка {index + 1}: {str(e)}")
                    continue
            
            db.commit()
        
        return {
            "records_processed": records_processed,
            "errors": errors,
            "warnings": warnings
        }
    
    async def _process_inventory(self, df: pd.DataFrame, warehouse_id: Optional[int] = None) -> Dict[str, Any]:
        """Обработка файла с инвентарем"""
        records_processed = 0
        errors = []
        warnings = []
        
        with get_db_context() as db:
            # Проверяем warehouse_id
            if warehouse_id:
                warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
                if not warehouse:
                    raise ValueError(f"Склад с ID {warehouse_id} не найден")
            else:
                # Берем первый склад по умолчанию
                warehouse = db.query(Warehouse).first()
                if not warehouse:
                    raise ValueError("Не найден ни один склад в системе")
                warehouse_id = warehouse.id
            
            for index, row in df.iterrows():
                try:
                    # Проверяем обязательные поля
                    if pd.isna(row.get('sku')):
                        errors.append(f"Строка {index + 1}: Отсутствует SKU")
                        continue
                    
                    # Находим продукт
                    product = db.query(Product).filter(Product.sku == str(row['sku'])).first()
                    if not product:
                        errors.append(f"Строка {index + 1}: Продукт с SKU {row['sku']} не найден")
                        continue
                    
                    # Проверяем, существует ли уже запись инвентаря
                    existing_inventory = db.query(InventoryItem).filter(
                        InventoryItem.product_id == product.id,
                        InventoryItem.warehouse_id == warehouse_id
                    ).first()
                    
                    if existing_inventory:
                        # Обновляем существующую запись
                        existing_inventory.current_stock = float(row.get('current_stock', 0)) if not pd.isna(row.get('current_stock')) else 0
                        existing_inventory.min_stock = float(row.get('min_stock', 0)) if not pd.isna(row.get('min_stock')) else 0
                        existing_inventory.max_stock = float(row.get('max_stock', 0)) if not pd.isna(row.get('max_stock')) else 0
                        existing_inventory.reorder_point = float(row.get('reorder_point', 0)) if not pd.isna(row.get('reorder_point')) else 0
                        existing_inventory.safety_stock = float(row.get('safety_stock', 0)) if not pd.isna(row.get('safety_stock')) else 0
                        existing_inventory.lead_time_days = int(row.get('lead_time_days', 0)) if not pd.isna(row.get('lead_time_days')) else 0
                    else:
                        # Создаем новую запись
                        inventory_item = InventoryItem(
                            product_id=product.id,
                            warehouse_id=warehouse_id,
                            current_stock=float(row.get('current_stock', 0)) if not pd.isna(row.get('current_stock')) else 0,
                            min_stock=float(row.get('min_stock', 0)) if not pd.isna(row.get('min_stock')) else 0,
                            max_stock=float(row.get('max_stock', 0)) if not pd.isna(row.get('max_stock')) else 0,
                            reorder_point=float(row.get('reorder_point', 0)) if not pd.isna(row.get('reorder_point')) else 0,
                            safety_stock=float(row.get('safety_stock', 0)) if not pd.isna(row.get('safety_stock')) else 0,
                            lead_time_days=int(row.get('lead_time_days', 0)) if not pd.isna(row.get('lead_time_days')) else 0
                        )
                        db.add(inventory_item)
                    
                    records_processed += 1
                    
                except Exception as e:
                    errors.append(f"Строка {index + 1}: {str(e)}")
                    continue
            
            db.commit()
        
        return {
            "records_processed": records_processed,
            "errors": errors,
            "warnings": warnings
        }
    
    async def _process_sales(self, df: pd.DataFrame, warehouse_id: Optional[int] = None) -> Dict[str, Any]:
        """Обработка файла с продажами"""
        records_processed = 0
        errors = []
        warnings = []
        
        with get_db_context() as db:
            # Проверяем warehouse_id
            if warehouse_id:
                warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
                if not warehouse:
                    raise ValueError(f"Склад с ID {warehouse_id} не найден")
            else:
                # Берем первый склад по умолчанию
                warehouse = db.query(Warehouse).first()
                if not warehouse:
                    raise ValueError("Не найден ни один склад в системе")
                warehouse_id = warehouse.id
            
            for index, row in df.iterrows():
                try:
                    # Проверяем обязательные поля
                    if pd.isna(row.get('sku')) or pd.isna(row.get('sale_date')) or pd.isna(row.get('quantity')):
                        errors.append(f"Строка {index + 1}: Отсутствуют обязательные поля")
                        continue
                    
                    # Находим продукт
                    product = db.query(Product).filter(Product.sku == str(row['sku'])).first()
                    if not product:
                        errors.append(f"Строка {index + 1}: Продукт с SKU {row['sku']} не найден")
                        continue
                    
                    # Парсим дату
                    try:
                        if isinstance(row['sale_date'], str):
                            sale_date = pd.to_datetime(row['sale_date'])
                        else:
                            sale_date = row['sale_date']
                    except:
                        errors.append(f"Строка {index + 1}: Неверный формат даты")
                        continue
                    
                    # Создаем запись о продаже
                    sale = Sale(
                        product_id=product.id,
                        warehouse_id=warehouse_id,
                        sale_date=sale_date,
                        quantity=float(row['quantity']),
                        revenue=float(row.get('revenue', 0)) if not pd.isna(row.get('revenue')) else 0,
                        cost=float(row.get('cost', 0)) if not pd.isna(row.get('cost')) else None,
                        customer_id=str(row.get('customer_id', '')) if not pd.isna(row.get('customer_id')) else None,
                        transaction_id=str(row.get('transaction_id', '')) if not pd.isna(row.get('transaction_id')) else None
                    )
                    
                    db.add(sale)
                    records_processed += 1
                    
                except Exception as e:
                    errors.append(f"Строка {index + 1}: {str(e)}")
                    continue
            
            db.commit()
        
        return {
            "records_processed": records_processed,
            "errors": errors,
            "warnings": warnings
        }
    
    async def _update_upload_status(self, file_path: str, status: str, records_processed: int, error_message: Optional[str] = None):
        """Обновление статуса загрузки файла"""
        try:
            with get_db_context() as db:
                upload_record = db.query(DataUpload).filter(DataUpload.file_path == file_path).first()
                if upload_record:
                    upload_record.status = status
                    upload_record.records_processed = records_processed
                    upload_record.error_message = error_message
                    db.commit()
        except Exception as e:
            logger.error(f"Ошибка обновления статуса загрузки: {e}")

# Создание экземпляра сервиса
file_processor = FileProcessor()
