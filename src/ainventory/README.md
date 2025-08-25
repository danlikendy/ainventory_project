# AInventory Backend API

Полноценный FastAPI backend для системы управления инвентарем и прогнозирования спроса.

## 🚀 Возможности

- **Загрузка данных**: Поддержка Excel (.xlsx, .xls) и CSV файлов
- **Управление инвентарем**: CRUD операции для товаров, складов, категорий
- **Прогнозирование спроса**: Интеграция с Prophet для ML-прогнозов
- **Аналитика**: Детальные отчеты по продажам, инвентарю и прогнозам
- **RESTful API**: Полноценный REST API с валидацией данных

## 📁 Структура проекта

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

## 🗄️ Модели данных

### Основные сущности:
- **Warehouse** - Склады
- **Category** - Категории товаров
- **Brand** - Бренды
- **Product** - Продукты
- **InventoryItem** - Остатки на складах
- **Sale** - Продажи
- **Forecast** - Прогнозы спроса
- **DataUpload** - Загруженные файлы

## 🔌 API Endpoints

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
Аналитика по продажам
- **Фильтры**: `start_date`, `end_date`, `warehouse_id`, `category_id`

#### GET `/sales/trends`
Тренды продаж по периодам
- **Параметры**: `period`, `start_date`, `end_date`, `warehouse_id`

#### GET `/inventory/overview`
Аналитика по инвентарю

#### GET `/dashboard/summary`
Сводка для дашборда

#### GET `/reports/inventory-status`
Отчет по статусу инвентаря

#### GET `/reports/sales-performance`
Отчет по эффективности продаж

## 📊 Форматы данных

### Продукты (products)
```csv
sku,name,description,category,brand,unit_cost,unit_price,weight,dimensions
PROD001,Название продукта,Описание,Электроника,Generic,100.0,150.0,0.5,10x5x2 см
```

### Инвентарь (inventory)
```csv
sku,current_stock,min_stock,max_stock,reorder_point,safety_stock,lead_time_days
PROD001,50.0,10.0,100.0,15.0,5.0,7
```

### Продажи (sales)
```csv
sku,sale_date,quantity,revenue,cost,customer_id,transaction_id
PROD001,2024-01-15,5.0,750.0,500.0,CUST001,TXN001
```

## 🚀 Запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных
```bash
# Создайте PostgreSQL базу данных
createdb ainventory

# Скопируйте env.example в .env и настройте DATABASE_URL
cp env.example .env
```

### 3. Запуск сервера
```bash
# Из корня проекта
python -m src.ainventory.api.main

# Или с uvicorn
uvicorn src.ainventory.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Документация API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Конфигурация

Основные настройки в `config.py`:

- **База данных**: URL, пул соединений
- **API**: хост, порт, CORS
- **Файлы**: максимальный размер, директория загрузок
- **Прогнозирование**: настройки Prophet
- **Инвентарь**: параметры безопасности

## 📝 Примеры использования

### Загрузка файла с продуктами
```bash
curl -X POST "http://localhost:8000/api/v1/data/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@products.xlsx" \
  -F "file_type=products"
```

### Получение аналитики по продажам
```bash
curl "http://localhost:8000/api/v1/analytics/sales/overview?start_date=2024-01-01&end_date=2024-01-31"
```

### Генерация прогноза
```bash
curl -X POST "http://localhost:8000/api/v1/forecasts/generate?product_id=1&warehouse_id=1&forecast_horizon=30"
```

## 🧪 Тестирование

```bash
# Запуск тестов
pytest tests/

# С покрытием
pytest --cov=src/ainventory tests/
```

## 🔒 Безопасность

- Валидация всех входных данных через Pydantic
- Ограничение размера загружаемых файлов
- Проверка типов файлов
- Логирование всех операций

## 📈 Производительность

- Асинхронная обработка файлов
- Пул соединений с базой данных
- Индексы для быстрого поиска
- Пагинация для больших списков

## 🤝 Разработка

### Добавление новых endpoints
1. Создайте роутер в `api/routers/`
2. Добавьте схемы в `schemas.py`
3. Подключите роутер в `main.py`

### Добавление новых моделей
1. Создайте модель в `database/models.py`
2. Добавьте схемы в `schemas.py`
3. Обновите миграции

## 📚 Дополнительные ресурсы

- [FastAPI документация](https://fastapi.tiangolo.com/)
- [SQLAlchemy документация](https://docs.sqlalchemy.org/)
- [Prophet документация](https://facebook.github.io/prophet/)
- [Pydantic документация](https://pydantic-docs.helpmanual.io/)
