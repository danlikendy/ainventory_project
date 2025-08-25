from .connection import engine, Base, get_db_context
from .models import *
import logging

logger = logging.getLogger(__name__)

async def init_db():
    """Инициализация базы данных"""
    try:
        # Создание всех таблиц
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Создание начальных данных
        await create_initial_data()
        logger.info("Initial data created successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

async def create_initial_data():
    """Создание начальных данных"""
    from .connection import get_db_context
    
    with get_db_context() as db:
        # Проверяем, есть ли уже данные
        if db.query(Warehouse).count() > 0:
            logger.info("Initial data already exists, skipping...")
            return
        
        # Создаем склады
        warehouses = [
            Warehouse(name="Основной склад", location="Москва", capacity=10000),
            Warehouse(name="Региональный склад", location="Санкт-Петербург", capacity=5000),
        ]
        
        for warehouse in warehouses:
            db.add(warehouse)
        
        # Создаем категории
        categories = [
            Category(name="Электроника", description="Электронные устройства"),
            Category(name="Одежда", description="Одежда и обувь"),
            Category(name="Книги", description="Книги и печатная продукция"),
        ]
        
        for category in categories:
            db.add(category)
        
        # Создаем бренды
        brands = [
            Brand(name="Generic", description="Универсальный бренд"),
            Brand(name="Premium", description="Премиум бренд"),
        ]
        
        for brand in brands:
            db.add(brand)
        
        db.commit()
        logger.info("Initial data created: warehouses, categories, brands")

def reset_db():
    """Сброс базы данных (только для разработки)"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables recreated successfully")
        
    except Exception as e:
        logger.error(f"Database reset failed: {e}")
        raise
