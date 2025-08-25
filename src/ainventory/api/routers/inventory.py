from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
import logging

from ..database.connection import get_db
from ..database.models import InventoryItem, Product, Warehouse, Category, Brand
from ..schemas import (
    InventoryItemResponse, InventoryItemCreate, InventoryItemUpdate,
    SearchParams, PaginatedResponse, InventoryAnalytics
)

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
async def get_inventory(
    search: Optional[str] = Query(None, description="Поиск по SKU или названию"),
    warehouse_id: Optional[int] = Query(None, description="Фильтр по складу"),
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    brand_id: Optional[int] = Query(None, description="Фильтр по бренду"),
    low_stock: Optional[bool] = Query(None, description="Только товары с низким остатком"),
    out_of_stock: Optional[bool] = Query(None, description="Только товары без остатка"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество записей на странице"),
    db: Session = Depends(get_db)
):
    """Получение списка товаров на складах с пагинацией и фильтрацией"""
    try:
        query = db.query(InventoryItem).join(Product).join(Warehouse)
        
        # Применяем фильтры
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.sku.ilike(search_term),
                    Product.name.ilike(search_term)
                )
            )
        
        if warehouse_id:
            query = query.filter(InventoryItem.warehouse_id == warehouse_id)
        
        if category_id:
            query = query.join(Category).filter(Product.category_id == category_id)
        
        if brand_id:
            query = query.join(Brand).filter(Product.brand_id == brand_id)
        
        if low_stock:
            query = query.filter(
                InventoryItem.current_stock <= InventoryItem.min_stock
            )
        
        if out_of_stock:
            query = query.filter(InventoryItem.current_stock == 0)
        
        # Получаем общее количество
        total = query.count()
        
        # Применяем пагинацию
        items = query.offset((page - 1) * limit).limit(limit).all()
        
        # Вычисляем количество страниц
        pages = (total + limit - 1) // limit
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения инвентаря: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/{item_id}", response_model=InventoryItemResponse)
async def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """Получение конкретного товара на складе"""
    try:
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Товар на складе не найден")
        
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения товара {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/", response_model=InventoryItemResponse)
async def create_inventory_item(
    item: InventoryItemCreate,
    db: Session = Depends(get_db)
):
    """Создание новой записи инвентаря"""
    try:
        # Проверяем, существует ли уже запись для этого продукта на этом складе
        existing_item = db.query(InventoryItem).filter(
            and_(
                InventoryItem.product_id == item.product_id,
                InventoryItem.warehouse_id == item.warehouse_id
            )
        ).first()
        
        if existing_item:
            raise HTTPException(
                status_code=400,
                detail="Запись для этого продукта на данном складе уже существует"
            )
        
        # Проверяем существование продукта и склада
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        
        warehouse = db.query(Warehouse).filter(Warehouse.id == item.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=404, detail="Склад не найден")
        
        # Создаем новую запись
        inventory_item = InventoryItem(**item.dict())
        db.add(inventory_item)
        db.commit()
        db.refresh(inventory_item)
        
        return inventory_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка создания записи инвентаря: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.put("/{item_id}", response_model=InventoryItemResponse)
async def update_inventory_item(
    item_id: int,
    item_update: InventoryItemUpdate,
    db: Session = Depends(get_db)
):
    """Обновление записи инвентаря"""
    try:
        inventory_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not inventory_item:
            raise HTTPException(status_code=404, detail="Товар на складе не найден")
        
        # Обновляем только переданные поля
        update_data = item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(inventory_item, field, value)
        
        db.commit()
        db.refresh(inventory_item)
        
        return inventory_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления товара {item_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.delete("/{item_id}")
async def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """Удаление записи инвентаря"""
    try:
        inventory_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not inventory_item:
            raise HTTPException(status_code=404, detail="Товар на складе не найден")
        
        db.delete(inventory_item)
        db.commit()
        
        return {"message": "Запись инвентаря успешно удалена"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления товара {item_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/{item_id}/adjust")
async def adjust_stock(
    item_id: int,
    quantity: float = Query(..., description="Количество для изменения (положительное - добавление, отрицательное - списание)"),
    reason: str = Query(..., description="Причина изменения остатка"),
    db: Session = Depends(get_db)
):
    """Корректировка остатка товара на складе"""
    try:
        inventory_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not inventory_item:
            raise HTTPException(status_code=404, detail="Товар на складе не найден")
        
        # Проверяем, что после списания остаток не станет отрицательным
        new_stock = inventory_item.current_stock + quantity
        if new_stock < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара для списания. Доступно: {inventory_item.current_stock}"
            )
        
        # Обновляем остаток
        inventory_item.current_stock = new_stock
        
        # TODO: Добавить логирование изменений остатков
        
        db.commit()
        db.refresh(inventory_item)
        
        return {
            "message": "Остаток успешно скорректирован",
            "old_stock": inventory_item.current_stock - quantity,
            "new_stock": inventory_item.current_stock,
            "change": quantity
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка корректировки остатка товара {item_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/analytics/overview", response_model=InventoryAnalytics)
async def get_inventory_analytics(db: Session = Depends(get_db)):
    """Получение аналитики по инвентарю"""
    try:
        # Общее количество товаров
        total_products = db.query(InventoryItem).count()
        
        # Товары с низким остатком
        low_stock_items = db.query(InventoryItem).filter(
            InventoryItem.current_stock <= InventoryItem.min_stock
        ).count()
        
        # Товары без остатка
        out_of_stock_items = db.query(InventoryItem).filter(
            InventoryItem.current_stock == 0
        ).count()
        
        # Общая стоимость инвентаря
        total_value = db.query(
            func.sum(InventoryItem.current_stock * Product.unit_cost)
        ).join(Product).filter(
            Product.unit_cost.isnot(None)
        ).scalar() or 0
        
        # Средний оборот (упрощенный расчет)
        # TODO: Реализовать более сложную логику расчета оборота
        
        return InventoryAnalytics(
            total_products=total_products,
            low_stock_items=low_stock_items,
            out_of_stock_items=out_of_stock_items,
            total_value=total_value,
            average_turnover=0.0  # Пока не реализовано
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения аналитики инвентаря: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/warehouses/{warehouse_id}/summary")
async def get_warehouse_summary(warehouse_id: int, db: Session = Depends(get_db)):
    """Получение сводки по складу"""
    try:
        warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=404, detail="Склад не найден")
        
        # Статистика по складу
        total_items = db.query(InventoryItem).filter(
            InventoryItem.warehouse_id == warehouse_id
        ).count()
        
        total_value = db.query(
            func.sum(InventoryItem.current_stock * Product.unit_cost)
        ).join(Product).filter(
            and_(
                InventoryItem.warehouse_id == warehouse_id,
                Product.unit_cost.isnot(None)
            )
        ).scalar() or 0
        
        low_stock_count = db.query(InventoryItem).filter(
            and_(
                InventoryItem.warehouse_id == warehouse_id,
                InventoryItem.current_stock <= InventoryItem.min_stock
            )
        ).count()
        
        return {
            "warehouse": {
                "id": warehouse.id,
                "name": warehouse.name,
                "location": warehouse.location
            },
            "summary": {
                "total_items": total_items,
                "total_value": total_value,
                "low_stock_count": low_stock_count
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения сводки по складу {warehouse_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
