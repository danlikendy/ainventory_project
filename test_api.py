#!/usr/bin/env python3
"""
Скрипт для тестирования AInventory API
"""

import requests
import json
import time
from pathlib import Path

# Конфигурация
API_BASE_URL = "http://localhost:8000/api/v1"
EXAMPLES_DIR = Path("examples")

def test_health():
    """Тест health check endpoint"""
    print("🏥 Тестирование health check...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
            return True
        else:
            print(f"❌ Health check: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к API. Убедитесь, что сервер запущен.")
        return False

def test_templates():
    """Тест получения шаблонов файлов"""
    print("\n📋 Тестирование получения шаблонов...")
    try:
        response = requests.get(f"{API_BASE_URL}/data/templates")
        if response.status_code == 200:
            templates = response.json()
            print("✅ Шаблоны получены:")
            for file_type, template in templates.items():
                print(f"   {file_type}: {len(template['columns'])} колонок")
            return True
        else:
            print(f"❌ Ошибка получения шаблонов: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_file_upload(file_path, file_type):
    """Тест загрузки файла"""
    print(f"\n📁 Тестирование загрузки файла: {file_path.name}")
    
    if not file_path.exists():
        print(f"❌ Файл не найден: {file_path}")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'text/csv')}
            data = {'file_type': file_type}
            
            response = requests.post(
                f"{API_BASE_URL}/data/upload",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Файл загружен: {result['message']}")
                print(f"   ID файла: {result['file_id']}")
                return True
            else:
                print(f"❌ Ошибка загрузки: {response.status_code}")
                print(f"   Детали: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_uploads_list():
    """Тест получения списка загруженных файлов"""
    print("\n📋 Тестирование получения списка загрузок...")
    try:
        response = requests.get(f"{API_BASE_URL}/data/uploads")
        if response.status_code == 200:
            uploads = response.json()
            print(f"✅ Загрузок найдено: {len(uploads)}")
            for upload in uploads[:3]:  # Показываем первые 3
                print(f"   {upload['filename']} - {upload['status']}")
            return True
        else:
            print(f"❌ Ошибка получения списка: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_inventory_analytics():
    """Тест получения аналитики инвентаря"""
    print("\n📊 Тестирование аналитики инвентаря...")
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/inventory/overview")
        if response.status_code == 200:
            analytics = response.json()
            print("✅ Аналитика инвентаря получена:")
            print(f"   Всего товаров: {analytics['total_products']}")
            print(f"   Низкий остаток: {analytics['low_stock_items']}")
            print(f"   Нет остатка: {analytics['out_of_stock_items']}")
            return True
        else:
            print(f"❌ Ошибка получения аналитики: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_dashboard_summary():
    """Тест получения сводки дашборда"""
    print("\n📈 Тестирование сводки дашборда...")
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/dashboard/summary")
        if response.status_code == 200:
            summary = response.json()
            print("✅ Сводка дашборда получена:")
            print(f"   Продажи (30 дней): {summary['sales']['recent_sales']}")
            print(f"   Выручка: {summary['sales']['recent_revenue']}")
            print(f"   Товаров в инвентаре: {summary['inventory']['total_products']}")
            return True
        else:
            print(f"❌ Ошибка получения сводки: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование AInventory API")
    print("=" * 50)
    
    # Проверяем доступность API
    if not test_health():
        return
    
    # Тестируем базовые endpoints
    test_templates()
    
    # Тестируем загрузку файлов
    if EXAMPLES_DIR.exists():
        print("\n📁 Тестирование загрузки файлов...")
        
        # Загружаем продукты
        products_file = EXAMPLES_DIR / "sample_products.csv"
        if products_file.exists():
            test_file_upload(products_file, "products")
            time.sleep(2)  # Ждем обработки
        
        # Загружаем инвентарь
        inventory_file = EXAMPLES_DIR / "sample_inventory.csv"
        if inventory_file.exists():
            test_file_upload(inventory_file, "inventory")
            time.sleep(2)  # Ждем обработки
        
        # Загружаем продажи
        sales_file = EXAMPLES_DIR / "sample_sales.csv"
        if sales_file.exists():
            test_file_upload(sales_file, "sales")
            time.sleep(2)  # Ждем обработки
    
    # Тестируем получение данных
    test_uploads_list()
    test_inventory_analytics()
    test_dashboard_summary()
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")
    print("\n📚 Документация API доступна по адресу:")
    print("   http://localhost:8000/docs")
    print("\n🔍 ReDoc доступен по адресу:")
    print("   http://localhost:8000/redoc")

if __name__ == "__main__":
    main()
