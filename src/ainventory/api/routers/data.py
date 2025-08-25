from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from pathlib import Path
import logging

from ..database.connection import get_db
from ..database.models import DataUpload
from ..services.file_processor import file_processor
from ..schemas import FileUploadRequest, FileUploadResponse, DataUploadResponse
from ..config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    file_type: str = Form(..., description="Тип данных: products, inventory, sales"),
    warehouse_id: Optional[int] = Form(None, description="ID склада (для inventory и sales)"),
    category_id: Optional[int] = Form(None, description="ID категории (для products)"),
    db: Session = Depends(get_db)
):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Имя файла не указано")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.xlsx', '.xls', '.csv']:
            raise HTTPException(
                status_code=400, 
                detail="Неподдерживаемый формат файла. Используйте Excel (.xlsx, .xls) или CSV"
            )
        
        if file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"Файл слишком большой. Максимальный размер: {settings.max_file_size / (1024*1024):.1f} MB"
            )
        
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(exist_ok=True)
        
        timestamp = int(os.time.time())
        safe_filename = f"{timestamp}_{file.filename.replace(' ', '_')}"
        file_path = upload_dir / safe_filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        upload_record = DataUpload(
            filename=file.filename,
            file_path=str(file_path),
            file_size=file.size,
            file_type=file.content_type,
            status="uploaded"
        )
        db.add(upload_record)
        db.commit()
        db.refresh(upload_record)
        
        background_tasks.add_task(
            process_uploaded_file,
            str(file_path),
            file_type,
            warehouse_id,
            upload_record.id
        )
        
        return FileUploadResponse(
            success=True,
            message="Файл успешно загружен и поставлен в очередь на обработку",
            records_processed=0,
            file_id=upload_record.id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка загрузки файла: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

async def process_uploaded_file(file_path: str, file_type: str, warehouse_id: Optional[int], upload_id: int):
    try:
        logger.info(f"Начинаем обработку файла {file_path}")
        
        result = await file_processor.process_file(file_path, file_type, warehouse_id)
        
        logger.info(f"Файл {file_path} успешно обработан: {result['records_processed']} записей")
        
    except Exception as e:
        logger.error(f"Ошибка обработки файла {file_path}: {e}")
        # Обновляем статус на failed
        with get_db() as db:
            upload_record = db.query(DataUpload).filter(DataUpload.id == upload_id).first()
            if upload_record:
                upload_record.status = "failed"
                upload_record.error_message = str(e)
                db.commit()

@router.get("/uploads", response_model=List[DataUploadResponse])
async def get_uploads(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Получение списка загруженных файлов"""
    try:
        query = db.query(DataUpload)
        
        if status:
            query = query.filter(DataUpload.status == status)
        
        uploads = query.order_by(DataUpload.upload_date.desc()).offset(offset).limit(limit).all()
        
        return uploads
        
    except Exception as e:
        logger.error(f"Ошибка получения списка загрузок: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/uploads/{upload_id}", response_model=DataUploadResponse)
async def get_upload(upload_id: int, db: Session = Depends(get_db)):
    """Получение информации о конкретной загрузке"""
    try:
        upload = db.query(DataUpload).filter(DataUpload.id == upload_id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Загрузка не найдена")
        
        return upload
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения загрузки {upload_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.delete("/uploads/{upload_id}")
async def delete_upload(upload_id: int, db: Session = Depends(get_db)):
    """Удаление загрузки и файла"""
    try:
        upload = db.query(DataUpload).filter(DataUpload.id == upload_id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Загрузка не найдена")
        
        # Удаляем файл
        try:
            if os.path.exists(upload.file_path):
                os.remove(upload.file_path)
        except Exception as e:
            logger.warning(f"Не удалось удалить файл {upload.file_path}: {e}")
        
        # Удаляем запись из базы
        db.delete(upload)
        db.commit()
        
        return {"message": "Загрузка успешно удалена"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления загрузки {upload_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/uploads/{upload_id}/retry")
async def retry_upload(upload_id: int, db: Session = Depends(get_db)):
    """Повторная попытка обработки файла"""
    try:
        upload = db.query(DataUpload).filter(DataUpload.id == upload_id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Загрузка не найдена")
        
        if upload.status not in ["failed", "uploaded"]:
            raise HTTPException(status_code=400, detail="Файл уже обработан или обрабатывается")
        
        # Определяем тип файла по имени или расширению
        file_type = "products"  # По умолчанию
        if "inventory" in upload.filename.lower() or "stock" in upload.filename.lower():
            file_type = "inventory"
        elif "sales" in upload.filename.lower() or "продажи" in upload.filename.lower():
            file_type = "sales"
        
        # Сбрасываем статус
        upload.status = "uploaded"
        upload.error_message = None
        db.commit()
        
        # Запускаем обработку
        import asyncio
        asyncio.create_task(
            process_uploaded_file(
                upload.file_path,
                file_type,
                None,  # warehouse_id будет определен автоматически
                upload.id
            )
        )
        
        return {"message": "Файл поставлен в очередь на повторную обработку"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка повторной обработки загрузки {upload_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/templates")
async def get_templates():
    """Получение шаблонов файлов для загрузки"""
    return {
        "products": {
            "columns": ["sku", "name", "description", "category", "brand", "unit_cost", "unit_price", "weight", "dimensions"],
            "required": ["sku", "name"],
            "example": {
                "sku": "PROD001",
                "name": "Название продукта",
                "description": "Описание продукта",
                "category": "Электроника",
                "brand": "Generic",
                "unit_cost": 100.0,
                "unit_price": 150.0,
                "weight": 0.5,
                "dimensions": "10x5x2 см"
            }
        },
        "inventory": {
            "columns": ["sku", "current_stock", "min_stock", "max_stock", "reorder_point", "safety_stock", "lead_time_days"],
            "required": ["sku"],
            "example": {
                "sku": "PROD001",
                "current_stock": 50.0,
                "min_stock": 10.0,
                "max_stock": 100.0,
                "reorder_point": 15.0,
                "safety_stock": 5.0,
                "lead_time_days": 7
            }
        },
        "sales": {
            "columns": ["sku", "sale_date", "quantity", "revenue", "cost", "customer_id", "transaction_id"],
            "required": ["sku", "sale_date", "quantity"],
            "example": {
                "sku": "PROD001",
                "sale_date": "2024-01-15",
                "quantity": 5.0,
                "revenue": 750.0,
                "cost": 500.0,
                "customer_id": "CUST001",
                "transaction_id": "TXN001"
            }
        }
    }
