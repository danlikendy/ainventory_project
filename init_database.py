#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных AInventory
"""

import os
import sys
from pathlib import Path

# Добавляем src в путь для импорта
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Инициализация базы данных"""
    print("🗄️ Инициализация базы данных AInventory")
    print("=" * 50)
    
    try:
        # Импортируем модули
        from ainventory.database.init_db import init_db
        import asyncio
        
        print("📦 Импорт модулей... OK")
        
        # Инициализируем базу данных
        print("🔧 Создание таблиц...")
        asyncio.run(init_db())
        
        print("✅ База данных успешно инициализирована!")
        print("\n📊 Созданы таблицы:")
        print("   - warehouses (склады)")
        print("   - categories (категории)")
        print("   - brands (бренды)")
        print("   - products (продукты)")
        print("   - inventory_items (инвентарь)")
        print("   - sales (продажи)")
        print("   - forecasts (прогнозы)")
        print("   - data_uploads (загрузки файлов)")
        
        print("\n🏪 Начальные данные:")
        print("   - 2 склада (Основной, Региональный)")
        print("   - 3 категории (Электроника, Одежда, Книги)")
        print("   - 2 бренда (Generic, Premium)")
        
        print("\n🚀 Система готова к работе!")
        print("\n📚 Документация API: http://localhost:8000/docs")
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что все зависимости установлены:")
        print("   pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        print("\n🔍 Возможные причины:")
        print("   1. PostgreSQL не запущен")
        print("   2. Неверные настройки подключения")
        print("   3. База данных не создана")
        print("\n💡 Решения:")
        print("   1. Запустите PostgreSQL: sudo systemctl start postgresql")
        print("   2. Создайте БД: createdb ainventory")
        print("   3. Проверьте DATABASE_URL в .env файле")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
