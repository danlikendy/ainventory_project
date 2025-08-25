from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Основные настройки
    app_name: str = "AInventory"
    version: str = "1.0.0"
    debug: bool = False
    
    # База данных
    database_url: str = "postgresql://ainventory:ainventory@localhost:5432/ainventory"
    database_echo: bool = False
    
    # API настройки
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Временные настройки
    timezone: str = "UTC"
    forecast_horizon_days: int = 30
    
    # Пути к файлам
    upload_dir: str = "uploads"
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    
    # Настройки прогнозирования
    prophet_seasonality_mode: str = "multiplicative"
    prophet_changepoint_prior_scale: float = 0.05
    prophet_seasonality_prior_scale: float = 10.0
    
    # Настройки инвентаря
    default_safety_stock_days: int = 7
    default_reorder_point_multiplier: float = 1.2
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Создание экземпляра настроек
settings = Settings()

# Создание директории для загрузок если её нет
os.makedirs(settings.upload_dir, exist_ok=True)
