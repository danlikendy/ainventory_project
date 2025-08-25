# AInventory - Система управления инвентарем и прогнозирования спроса

Полноценная система для управления складскими запасами, анализа продаж и прогнозирования спроса с использованием машинного обучения

## Возможности

- **Управление инвентарем**: Полный контроль над товарными запасами
- **Аналитика продаж**: Детальные отчеты и тренды
- **Прогнозирование спроса**: ML-модели для предсказания спроса
- **Загрузка данных**: Поддержка Excel и CSV файлов
- **Современный веб-интерфейс**: React + Next.js frontend
- **Быстрый API**: FastAPI backend с автоматической документацией
- **Надежная БД**: PostgreSQL с оптимизированными запросами

## Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Структура проекта

```
ainventory_project/
├── frontend/                 # Next.js frontend
│   ├── components/          # React компоненты
│   ├── app/                 # Next.js 13+ app router
│   └── package.json         # Node.js зависимости
├── src/ainventory/          # Python backend
│   ├── api/                 # FastAPI приложение
│   ├── database/            # Модели и подключение к БД
│   ├── services/            # Бизнес-логика
│   └── forecasting/         # ML модели
├── docker-compose.yml       # Docker конфигурация
├── requirements.txt         # Python зависимости
└── Makefile                 # Команды для управления
```

## Быстрый старт

### 1. Клонирование и настройка
```bash
git clone <repository-url>
cd ainventory_project

# Установка зависимостей
make setup
```

### 2. Запуск в режиме разработки
```bash
# Запуск всех сервисов
make run

# Или по отдельности:
make run-backend    # Backend API на http://localhost:8000
make run-frontend   # Frontend на http://localhost:3000
```

### 3. Доступ к системе
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Запуск с Docker

### 1. Сборка и запуск
```bash
# Сборка образов
make docker-build

# Запуск сервисов
make docker-run

# Просмотр логов
make docker-logs

# Остановка
make docker-stop
```

### 2. Доступ к сервисам
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: localhost:5432

## Загрузка данных

### Поддерживаемые форматы
- **Excel**: .xlsx, .xls
- **CSV**: UTF-8, CP1251, Latin1

### Типы данных
1. **Продукты** (`products`): SKU, название, категория, бренд, цены
2. **Инвентарь** (`inventory`): остатки, минимальные уровни, точки перезаказа
3. **Продажи** (`sales`): дата, количество, выручка, склад

## API Endpoints

### Основные эндпоинты
- `POST /api/v1/upload` - Загрузка файлов
- `GET /api/v1/inventory` - Управление инвентарем
- `GET /api/v1/forecasts` - Прогнозы спроса
- `GET /api/v1/analytics` - Аналитика и отчеты

### Документация API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Разработка

### Требования
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+
- Docker & Docker Compose

### Установка зависимостей
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Запуск тестов
```bash
make test
```

### Линтинг и форматирование
```bash
make lint
make format
```

## Конфигурация

Основные настройки в файле `env.example`:
- Database URL
- API настройки
- CORS настройки
- Параметры прогнозирования
