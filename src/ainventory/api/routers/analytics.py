from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, extract
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from ..database.connection import get_db
from ..database.models import Sale, Product, InventoryItem, Warehouse, Category, Brand, Forecast
from ..schemas import SalesAnalytics, InventoryAnalytics, ForecastAnalytics

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/sales/overview", response_model=SalesAnalytics)
async def get_sales_analytics(
    start_date: Optional[datetime] = Query(None, description="Начальная дата"),
    end_date: Optional[datetime] = Query(None, description="Конечная дата"),
    warehouse_id: Optional[int] = Query(None, description="Фильтр по складу"),
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    db: Session = Depends(get_db)
):
    """Получение аналитики по продажам"""
    try:
        query = db.query(Sale).join(Product)
        
        # Применяем фильтры по датам
        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
        
        # Фильтры по складу и категории
        if warehouse_id:
            query = query.filter(Sale.warehouse_id == warehouse_id)
        if category_id:
            query = query.join(Category).filter(Product.category_id == category_id)
        
        # Общее количество продаж
        total_sales = query.count()
        
        # Общая выручка
        total_revenue = query.with_entities(func.sum(Sale.revenue)).scalar() or 0
        
        # Общее количество проданных товаров
        total_quantity = query.with_entities(func.sum(Sale.quantity)).scalar() or 0
        
        # Средний чек
        average_order_value = total_revenue / total_sales if total_sales > 0 else 0
        
        # Топ продуктов по выручке
        top_products_query = query.with_entities(
            Product.sku,
            Product.name,
            func.sum(Sale.revenue).label('total_revenue'),
            func.sum(Sale.quantity).label('total_quantity')
        ).group_by(Product.id, Product.sku, Product.name).order_by(
            desc(func.sum(Sale.revenue))
        ).limit(10)
        
        top_products = []
        for row in top_products_query.all():
            top_products.append({
                "sku": row.sku,
                "name": row.name,
                "total_revenue": float(row.total_revenue),
                "total_quantity": float(row.total_quantity)
            })
        
        return SalesAnalytics(
            total_sales=total_sales,
            total_revenue=total_revenue,
            total_quantity=total_quantity,
            average_order_value=average_order_value,
            top_products=top_products
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения аналитики продаж: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/sales/trends")
async def get_sales_trends(
    period: str = Query("month", description="Период группировки: day, week, month"),
    start_date: datetime = Query(..., description="Начальная дата"),
    end_date: datetime = Query(..., description="Конечная дата"),
    warehouse_id: Optional[int] = Query(None, description="Фильтр по складу"),
    db: Session = Depends(get_db)
):
    """Получение трендов продаж по периодам"""
    try:
        query = db.query(Sale).join(Product)
        
        # Применяем фильтры
        query = query.filter(
            and_(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            )
        )
        
        if warehouse_id:
            query = query.filter(Sale.warehouse_id == warehouse_id)
        
        # Группируем по периоду
        if period == "day":
            group_by = func.date(Sale.sale_date)
        elif period == "week":
            group_by = func.date_trunc('week', Sale.sale_date)
        elif period == "month":
            group_by = func.date_trunc('month', Sale.sale_date)
        else:
            raise HTTPException(status_code=400, detail="Неподдерживаемый период группировки")
        
        trends = query.with_entities(
            group_by.label('period'),
            func.sum(Sale.revenue).label('revenue'),
            func.sum(Sale.quantity).label('quantity'),
            func.count(Sale.id).label('orders')
        ).group_by(group_by).order_by(group_by).all()
        
        result = []
        for trend in trends:
            result.append({
                "period": trend.period.isoformat() if hasattr(trend.period, 'isoformat') else str(trend.period),
                "revenue": float(trend.revenue),
                "quantity": float(trend.quantity),
                "orders": trend.orders
            })
        
        return {
            "period": period,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "trends": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения трендов продаж: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/inventory/overview", response_model=InventoryAnalytics)
async def get_inventory_analytics(
    warehouse_id: Optional[int] = Query(None, description="Фильтр по складу"),
    db: Session = Depends(get_db)
):
    """Получение аналитики по инвентарю"""
    try:
        query = db.query(InventoryItem).join(Product)
        
        if warehouse_id:
            query = query.filter(InventoryItem.warehouse_id == warehouse_id)
        
        # Общее количество товаров
        total_products = query.count()
        
        # Товары с низким остатком
        low_stock_items = query.filter(
            InventoryItem.current_stock <= InventoryItem.min_stock
        ).count()
        
        # Товары без остатка
        out_of_stock_items = query.filter(
            InventoryItem.current_stock == 0
        ).count()
        
        # Общая стоимость инвентаря
        total_value = query.with_entities(
            func.sum(InventoryItem.current_stock * Product.unit_cost)
        ).filter(Product.unit_cost.isnot(None)).scalar() or 0
        
        # TODO: Реализовать расчет среднего оборота
        average_turnover = 0.0
        
        return InventoryAnalytics(
            total_products=total_products,
            low_stock_items=low_stock_items,
            out_of_stock_items=out_of_stock_items,
            total_value=total_value,
            average_turnover=average_turnover
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения аналитики инвентаря: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/inventory/aging")
async def get_inventory_aging(
    warehouse_id: Optional[int] = Query(None, description="Фильтр по складу"),
    db: Session = Depends(get_db)
):
    """Получение анализа старения инвентаря"""
    try:
        query = db.query(InventoryItem).join(Product)
        
        if warehouse_id:
            query = query.filter(InventoryItem.warehouse_id == warehouse_id)
        
        # Группируем по диапазонам остатков
        aging_ranges = [
            (0, 0, "Нет остатка"),
            (0.01, 10, "0-10"),
            (10.01, 50, "10-50"),
            (50.01, 100, "50-100"),
            (100.01, 500, "100-500"),
            (500.01, float('inf'), "500+")
        ]
        
        result = []
        for min_val, max_val, label in aging_ranges:
            if max_val == float('inf'):
                count = query.filter(InventoryItem.current_stock > min_val).count()
            else:
                count = query.filter(
                    and_(
                        InventoryItem.current_stock > min_val,
                        InventoryItem.current_stock <= max_val
                    )
                ).count()
            
            result.append({
                "range": label,
                "count": count
            })
        
        return {
            "warehouse_id": warehouse_id,
            "aging_analysis": result
        }
        
    except Exception as e:
        logger.error(f"Ошибка получения анализа старения инвентаря: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/forecasts/overview", response_model=ForecastAnalytics)
async def get_forecast_analytics(db: Session = Depends(get_db)):
    """Получение аналитики по прогнозам"""
    try:
        # Общее количество прогнозов
        total_forecasts = db.query(Forecast).count()
        
        # Уникальные модели
        models_used = db.query(Forecast.model_name).distinct().all()
        models_used = [model[0] for model in models_used]
        
        # Дата следующего прогноза
        next_forecast = db.query(Forecast).order_by(desc(Forecast.forecast_date)).first()
        next_forecast_date = next_forecast.forecast_date if next_forecast else None
        
        # TODO: Реализовать расчет точности прогнозов
        average_accuracy = 0.0
        
        return ForecastAnalytics(
            total_forecasts=total_forecasts,
            average_accuracy=average_accuracy,
            models_used=models_used,
            next_forecast_date=next_forecast_date
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения аналитики прогнозов: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/dashboard/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Получение сводки для дашборда"""
    try:
        # Статистика по продажам (последние 30 дней)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_sales = db.query(Sale).filter(Sale.sale_date >= thirty_days_ago).count()
        recent_revenue = db.query(func.sum(Sale.revenue)).filter(Sale.sale_date >= thirty_days_ago).scalar() or 0
        
        # Статистика по инвентарю
        total_products = db.query(InventoryItem).count()
        low_stock_count = db.query(InventoryItem).filter(
            InventoryItem.current_stock <= InventoryItem.min_stock
        ).count()
        
        # Статистика по прогнозам
        total_forecasts = db.query(Forecast).count()
        
        # Топ категорий по продажам
        top_categories = db.query(
            Category.name,
            func.sum(Sale.revenue).label('revenue')
        ).join(Product).join(Sale).group_by(Category.id, Category.name).order_by(
            desc(func.sum(Sale.revenue))
        ).limit(5).all()
        
        top_categories_list = []
        for category in top_categories:
            top_categories_list.append({
                "name": category.name,
                "revenue": float(category.revenue)
            })
        
        return {
            "sales": {
                "recent_sales": recent_sales,
                "recent_revenue": recent_revenue,
                "period_days": 30
            },
            "inventory": {
                "total_products": total_products,
                "low_stock_count": low_stock_count
            },
            "forecasts": {
                "total_count": total_forecasts
            },
            "top_categories": top_categories_list
        }
        
    except Exception as e:
        logger.error(f"Ошибка получения сводки дашборда: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/reports/inventory-status")
async def generate_inventory_status_report(
    warehouse_id: Optional[int] = Query(None, description="Фильтр по складу"),
    include_zero_stock: bool = Query(True, description="Включать товары с нулевым остатком"),
    db: Session = Depends(get_db)
):
    """Генерация отчета по статусу инвентаря"""
    try:
        query = db.query(InventoryItem).join(Product).join(Warehouse)
        
        if warehouse_id:
            query = query.filter(InventoryItem.warehouse_id == warehouse_id)
        
        if not include_zero_stock:
            query = query.filter(InventoryItem.current_stock > 0)
        
        items = query.all()
        
        report_data = []
        for item in items:
            status = "OK"
            if item.current_stock == 0:
                status = "Out of Stock"
            elif item.current_stock <= item.min_stock:
                status = "Low Stock"
            elif item.current_stock >= item.max_stock:
                status = "Overstocked"
            
            report_data.append({
                "sku": item.product.sku,
                "name": item.product.name,
                "warehouse": item.warehouse.name,
                "current_stock": item.current_stock,
                "min_stock": item.min_stock,
                "max_stock": item.max_stock,
                "reorder_point": item.reorder_point,
                "status": status,
                "last_updated": item.last_updated.isoformat() if item.last_updated else None
            })
        
        return {
            "report_type": "inventory_status",
            "generated_at": datetime.now().isoformat(),
            "warehouse_id": warehouse_id,
            "total_items": len(report_data),
            "data": report_data
        }
        
    except Exception as e:
        logger.error(f"Ошибка генерации отчета по статусу инвентаря: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/reports/sales-performance")
async def generate_sales_performance_report(
    start_date: datetime = Query(..., description="Начальная дата"),
    end_date: datetime = Query(..., description="Конечная дата"),
    warehouse_id: Optional[int] = Query(None, description="Фильтр по складу"),
    db: Session = Depends(get_db)
):
    """Генерация отчета по эффективности продаж"""
    try:
        query = db.query(Sale).join(Product).join(Warehouse)
        
        query = query.filter(
            and_(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            )
        )
        
        if warehouse_id:
            query = query.filter(Sale.warehouse_id == warehouse_id)
        
        # Группируем по продуктам
        product_performance = query.with_entities(
            Product.sku,
            Product.name,
            func.sum(Sale.quantity).label('total_quantity'),
            func.sum(Sale.revenue).label('total_revenue'),
            func.avg(Sale.revenue / Sale.quantity).label('avg_unit_price'),
            func.count(Sale.id).label('order_count')
        ).group_by(Product.id, Product.sku, Product.name).order_by(
            desc(func.sum(Sale.revenue))
        ).all()
        
        report_data = []
        for perf in product_performance:
            report_data.append({
                "sku": perf.sku,
                "name": perf.name,
                "total_quantity": float(perf.total_quantity),
                "total_revenue": float(perf.total_revenue),
                "avg_unit_price": float(perf.avg_unit_price) if perf.avg_unit_price else 0,
                "order_count": perf.order_count
            })
        
        return {
            "report_type": "sales_performance",
            "generated_at": datetime.now().isoformat(),
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "warehouse_id": warehouse_id,
            "total_products": len(report_data),
            "data": report_data
        }
        
    except Exception as e:
        logger.error(f"Ошибка генерации отчета по эффективности продаж: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
