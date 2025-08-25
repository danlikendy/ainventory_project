#!/usr/bin/env python3
"""
Простой скрипт для запуска AInventory Backend API
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Импортируем и запускаем FastAPI приложение
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Создаем простое приложение для тестирования
app = FastAPI(
    title="AInventory API",
    description="Demand & Inventory Intelligence API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AInventory API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ainventory-api"}

@app.get("/test")
async def test():
    return {"message": "Backend is working correctly!"}

if __name__ == "__main__":
    print("🚀 Запуск AInventory Backend API...")
    print("📍 Хост: 0.0.0.0")
    print("🔌 Порт: 8000")
    print("📚 Документация: http://localhost:8000/docs")
    print("🔍 ReDoc: http://localhost:8000/redoc")
    print("-" * 50)
    
    uvicorn.run(
        "simple_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
