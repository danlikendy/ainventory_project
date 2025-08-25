# AInventory Backend API

Полноценный FastAPI backend для системы управления инвентарем и прогнозирования спроса.

## Возможности

- **Загрузка данных**: Поддержка Excel (.xlsx, .xls) и CSV файлов
- **Управление инвентарем**: CRUD операции для товаров, складов, категорий
- **Прогнозирование спроса**: Интеграция с Prophet для ML-прогнозов
- **Аналитика**: Детальные отчеты по продажам, инвентарю и прогнозам
- **RESTful API**: Полноценный REST API с валидацией данных

## Структура проекта

```
src/ainventory/
├── api/                    # FastAPI приложение
│   ├── main.py            # Основной сервер
│   ├── routers/           # API роутеры
│   │   ├── data.py        # Загрузка данных
│   │   ├── inventory.py   # Управление инвентарем
│   │   ├── forecasts.py   # Прогнозирование
│   │   └── analytics.py   # Аналитика и отчеты
│   └── schemas.py         # Pydantic схемы
├── database/              # База данных
│   ├── models.py          # SQLAlchemy модели
│   ├── connection.py      # Подключение к БД
│   └── init_db.py         # Инициализация БД
├── services/              # Бизнес-логика
│   └── file_processor.py  # Обработка файлов
├── forecasting/           # Модели прогнозирования
│   └── prophet_model.py   # Prophet интеграция
└── config.py              # Конфигурация
```

## Модели данных

### Основные сущности:
- **Warehouse** - Склады
- **Category** - Категории товаров
- **Brand** - Бренды
- **Product** - Продукты
- **InventoryItem** - Остатки на складах
- **Sale** - Продажи
- **Forecast** - Прогнозы спроса
- **DataUpload** - Загруженные файлы

## API Endpoints

### 1. Загрузка данных (`/api/v1/data/`)

#### POST `/upload`
Загрузка файла с данными
- **Параметры**: `file`, `file_type`, `warehouse_id`, `category_id`
- **Поддерживаемые типы**: `products`, `inventory`, `sales`
- **Форматы**: Excel (.xlsx, .xls), CSV

#### GET `/uploads`
Список загруженных файлов
- **Фильтры**: `status`, `limit`, `offset`

#### GET `/templates`
Шаблоны файлов для загрузки

### 2. Инвентарь (`/api/v1/inventory/`)

#### GET `/`
Список товаров на складах с фильтрацией
- **Фильтры**: `search`, `warehouse_id`, `category_id`, `brand_id`, `low_stock`, `out_of_stock`
- **Пагинация**: `page`, `limit`

#### POST `/`
Создание новой записи инвентаря

#### PUT `/{item_id}`
Обновление записи инвентаря

#### DELETE `/{item_id}`
Удаление записи инвентаря

#### POST `/{item_id}/adjust`
Корректировка остатка товара

#### GET `/analytics/overview`
Аналитика по инвентарю

### 3. Прогнозы (`/api/v1/forecasts/`)

#### GET `/`
Список прогнозов с фильтрацией
- **Фильтры**: `product_id`, `warehouse_id`, `model_name`, `start_date`, `end_date`

#### POST `/generate`
Генерация нового прогноза
- **Параметры**: `product_id`, `warehouse_id`, `forecast_horizon`, `model_name`

#### GET `/analytics/overview`
Аналитика по прогнозам

#### GET `/accuracy/evaluate`
Оценка точности прогнозов

### 4. Аналитика (`/api/v1/analytics/`)

#### GET `/sales/overview`
Обзор продаж

#### GET `/sales/trends`
Тренды продаж

#### GET `/inventory/overview`
Обзор инвентаря

#### GET `/inventory/aging`
Анализ старения инвентаря

#### GET `/dashboard/summary`
Сводка для дашборда

## Установка и запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных
```bash
# Создание .env файла
cp env.example .env

# Настройка DATABASE_URL в .env
```

### 3. Запуск
```bash
# Разработка
uvicorn src.ainventory.api.main:app --reload

# Продакшен
uvicorn src.ainventory.api.main:app --host 0.0.0.0 --port 8000
```

## Конфигурация

Основные настройки в `config.py`:
- Database URL
- API настройки
- CORS настройки
- Параметры прогнозирования

## Тестирование

```bash
pytest tests/
```

## Лицензия

MIT
