from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
import json

from ..database.connection import get_db
from ..database.models import Forecast, Product, InventoryItem, Sale
from ..schemas import (
    ForecastResponse, ForecastCreate, ForecastUpdate,
    SearchParams, PaginatedResponse, ForecastAnalytics
)
from ..forecasting.prophet_model import ProphetForecaster

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
async def get_forecasts(
    product_id: Optional[int] = Query(None, description="Фильтр по продукту"),
    warehouse_id: Optional[int] = Query(None, description="Фильтр по складу"),
    model_name: Optional[str] = Query(None, description="Фильтр по модели"),
    start_date: Optional[datetime] = Query(None, description="Начальная дата"),
    end_date: Optional[datetime] = Query(None, description="Конечная дата"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество записей на странице"),
    db: Session = Depends(get_db)
):
    """Получение списка прогнозов с пагинацией и фильтрацией"""
    try:
        query = db.query(Forecast).join(Product)
        
        # Применяем фильтры
        if product_id:
            query = query.filter(Forecast.product_id == product_id)
        
        if warehouse_id:
            query = query.filter(Forecast.warehouse_id == warehouse_id)
        
        if model_name:
            query = query.filter(Forecast.model_name == model_name)
        
        if start_date:
            query = query.filter(Forecast.forecast_date >= start_date)
        
        if end_date:
            query = query.filter(Forecast.forecast_date <= end_date)
        
        # Сортируем по дате прогноза (новые сначала)
        query = query.order_by(desc(Forecast.forecast_date))
        
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
        logger.error(f"Ошибка получения прогнозов: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/{forecast_id}", response_model=ForecastResponse)
async def get_forecast(forecast_id: int, db: Session = Depends(get_db)):
    """Получение конкретного прогноза"""
    try:
        forecast = db.query(Forecast).filter(Forecast.id == forecast_id).first()
        if not forecast:
            raise HTTPException(status_code=404, detail="Прогноз не найден")
        
        return forecast
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения прогноза {forecast_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/", response_model=ForecastResponse)
async def create_forecast(
    forecast: ForecastCreate,
    db: Session = Depends(get_db)
):
    """Создание нового прогноза"""
    try:
        # Проверяем существование продукта
        product = db.query(Product).filter(Product.id == forecast.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        
        # Проверяем, существует ли уже прогноз для этого продукта на эту дату
        existing_forecast = db.query(Forecast).filter(
            and_(
                Forecast.product_id == forecast.product_id,
                Forecast.warehouse_id == forecast.warehouse_id,
                Forecast.forecast_date == forecast.forecast_date,
                Forecast.model_name == forecast.model_name
            )
        ).first()
        
        if existing_forecast:
            raise HTTPException(
                status_code=400,
                detail="Прогноз для этого продукта на данную дату уже существует"
            )
        
        # Создаем новый прогноз
        new_forecast = Forecast(**forecast.dict())
        db.add(new_forecast)
        db.commit()
        db.refresh(new_forecast)
        
        return new_forecast
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка создания прогноза: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.put("/{forecast_id}", response_model=ForecastResponse)
async def update_forecast(
    forecast_id: int,
    forecast_update: ForecastUpdate,
    db: Session = Depends(get_db)
):
    """Обновление прогноза"""
    try:
        forecast = db.query(Forecast).filter(Forecast.id == forecast_id).first()
        if not forecast:
            raise HTTPException(status_code=404, detail="Прогноз не найден")
        
        # Обновляем только переданные поля
        update_data = forecast_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(forecast, field, value)
        
        db.commit()
        db.refresh(forecast)
        
        return forecast
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления прогноза {forecast_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.delete("/{forecast_id}")
async def delete_forecast(forecast_id: int, db: Session = Depends(get_db)):
    """Удаление прогноза"""
    try:
        forecast = db.query(Forecast).filter(Forecast.id == forecast_id).first()
        if not forecast:
            raise HTTPException(status_code=404, detail="Прогноз не найден")
        
        db.delete(forecast)
        db.commit()
        
        return {"message": "Прогноз успешно удален"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления прогноза {forecast_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/generate", response_model=Dict[str, Any])
async def generate_forecast(
    background_tasks: BackgroundTasks,
    product_id: int = Query(..., description="ID продукта"),
    warehouse_id: int = Query(..., description="ID склада"),
    forecast_horizon: int = Query(30, ge=1, le=365, description="Горизонт прогнозирования в днях"),
    model_name: str = Query("prophet", description="Название модели"),
    db: Session = Depends(get_db)
):
    """Генерация прогноза спроса для продукта"""
    try:
        # Проверяем существование продукта и склада
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        
        # Проверяем, есть ли данные о продажах для прогнозирования
        sales_count = db.query(Sale).filter(
            and_(
                Sale.product_id == product_id,
                Sale.warehouse_id == warehouse_id
            )
        ).count()
        
        if sales_count < 10:  # Минимум 10 записей для прогнозирования
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно данных для прогнозирования. Требуется минимум 10 записей о продажах, доступно: {sales_count}"
            )
        
        # Запускаем генерацию прогноза в фоне
        background_tasks.add_task(
            generate_forecast_background,
            product_id,
            warehouse_id,
            forecast_horizon,
            model_name
        )
        
        return {
            "message": "Прогноз поставлен в очередь на генерацию",
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "forecast_horizon": forecast_horizon,
            "model_name": model_name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка запуска генерации прогноза: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

async def generate_forecast_background(
    product_id: int,
    warehouse_id: int,
    forecast_horizon: int,
    model_name: str
):
    """Генерация прогноза в фоновом режиме"""
    try:
        logger.info(f"Начинаем генерацию прогноза для продукта {product_id} на складе {warehouse_id}")
        
        # Получаем данные о продажах
        with get_db() as db:
            sales_data = db.query(Sale).filter(
                and_(
                    Sale.product_id == product_id,
                    Sale.warehouse_id == warehouse_id
                )
            ).order_by(Sale.sale_date).all()
        
        if not sales_data:
            logger.error(f"Нет данных о продажах для продукта {product_id}")
            return
        
        # Подготавливаем данные для прогнозирования
        sales_df = prepare_sales_data(sales_data)
        
        # Генерируем прогноз
        if model_name == "prophet":
            forecaster = ProphetForecaster()
            forecast_result = await forecaster.forecast(sales_df, forecast_horizon)
        else:
            raise ValueError(f"Неподдерживаемая модель: {model_name}")
        
        # Сохраняем прогнозы в базу данных
        with get_db() as db:
            for date, value, lower, upper in forecast_result:
                forecast = Forecast(
                    product_id=product_id,
                    warehouse_id=warehouse_id,
                    forecast_date=date,
                    forecast_value=value,
                    confidence_lower=lower,
                    confidence_upper=upper,
                    model_name=model_name,
                    model_version="1.0",
                    features_used=json.dumps({"sales_history": len(sales_data)}),
                    accuracy_metrics=json.dumps({"model": model_name})
                )
                db.add(forecast)
            
            db.commit()
        
        logger.info(f"Прогноз для продукта {product_id} успешно сгенерирован и сохранен")
        
    except Exception as e:
        logger.error(f"Ошибка генерации прогноза для продукта {product_id}: {e}")

def prepare_sales_data(sales_data: List[Sale]) -> Any:
    """Подготовка данных о продажах для прогнозирования"""
    # TODO: Реализовать подготовку данных для Prophet
    # Пока возвращаем заглушку
    return sales_data

@router.get("/analytics/overview", response_model=ForecastAnalytics)
async def get_forecast_analytics(db: Session = Depends(get_db)):
    """Получение аналитики по прогнозам"""
    try:
        # Общее количество прогнозов
        total_forecasts = db.query(Forecast).count()
        
        # Уникальные модели
        models_used = db.query(Forecast.model_name).distinct().all()
        models_used = [model[0] for model in models_used]
        
        # Дата следующего прогноза
        next_forecast = db.query(Forecast).order_by(Forecast.forecast_date.desc()).first()
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

@router.get("/products/{product_id}/latest")
async def get_latest_product_forecast(
    product_id: int,
    warehouse_id: Optional[int] = Query(None, description="ID склада"),
    db: Session = Depends(get_db)
):
    """Получение последнего прогноза для продукта"""
    try:
        query = db.query(Forecast).filter(Forecast.product_id == product_id)
        
        if warehouse_id:
            query = query.filter(Forecast.warehouse_id == warehouse_id)
        
        latest_forecast = query.order_by(desc(Forecast.forecast_date)).first()
        
        if not latest_forecast:
            raise HTTPException(
                status_code=404,
                detail="Прогнозы для данного продукта не найдены"
            )
        
        return latest_forecast
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения последнего прогноза для продукта {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/accuracy/evaluate")
async def evaluate_forecast_accuracy(
    product_id: Optional[int] = Query(None, description="ID продукта"),
    warehouse_id: Optional[int] = Query(None, description="ID склада"),
    start_date: datetime = Query(..., description="Начальная дата для оценки"),
    end_date: datetime = Query(..., description="Конечная дата для оценки"),
    db: Session = Depends(get_db)
):
    """Оценка точности прогнозов"""
    try:
        # Получаем прогнозы за указанный период
        query = db.query(Forecast).filter(
            and_(
                Forecast.forecast_date >= start_date,
                Forecast.forecast_date <= end_date
            )
        )
        
        if product_id:
            query = query.filter(Forecast.product_id == product_id)
        
        if warehouse_id:
            query = query.filter(Forecast.warehouse_id == warehouse_id)
        
        forecasts = query.all()
        
        if not forecasts:
            raise HTTPException(
                status_code=404,
                detail="Прогнозы за указанный период не найдены"
            )
        
        # TODO: Реализовать расчет метрик точности
        # Пока возвращаем заглушку
        
        return {
            "message": "Оценка точности прогнозов",
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "forecasts_count": len(forecasts),
            "accuracy_metrics": {
                "mae": 0.0,  # Mean Absolute Error
                "rmse": 0.0,  # Root Mean Square Error
                "mape": 0.0   # Mean Absolute Percentage Error
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка оценки точности прогнозов: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
