#!/usr/bin/env python3
"""
Скрипт для запуска AInventory Backend API
"""

import uvicorn
import os
import sys
from pathlib import Path

# Добавляем src в путь для импорта
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Запуск FastAPI сервера"""
    
    # Настройки по умолчанию
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🚀 Запуск AInventory Backend API...")
    print(f"📍 Хост: {host}")
    print(f"🔌 Порт: {port}")
    print(f"🔄 Режим разработки: {reload}")
    print(f"📚 Документация: http://{host}:{port}/docs")
    print(f"🔍 ReDoc: http://{host}:{port}/redoc")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "ainventory.api.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
