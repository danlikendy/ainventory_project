# AInventory - Система управления инвентарем и прогнозирования спроса

Полноценная система для управления складскими запасами, анализа продаж и прогнозирования спроса с использованием машинного обучения.

## 🚀 Возможности

- **📊 Управление инвентарем**: Полный контроль над товарными запасами
- **📈 Аналитика продаж**: Детальные отчеты и тренды
- **🔮 Прогнозирование спроса**: ML-модели для предсказания спроса
- **📁 Загрузка данных**: Поддержка Excel и CSV файлов
- **🌐 Современный веб-интерфейс**: React + Next.js frontend
- **⚡ Быстрый API**: FastAPI backend с автоматической документацией
- **🗄️ Надежная БД**: PostgreSQL с оптимизированными запросами

## 🏗️ Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Структура проекта

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
├── examples/                # Примеры файлов для тестирования
├── docker-compose.yml       # Docker конфигурация
├── requirements.txt         # Python зависимости
└── Makefile                 # Команды для управления
```

## 🚀 Быстрый старт

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

## 🐳 Запуск с Docker

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

## 📊 Загрузка данных

### Поддерживаемые форматы
- **Excel**: .xlsx, .xls
- **CSV**: UTF-8, CP1251, Latin1

### Типы данных
1. **Продукты** (`products`): SKU, название, категория, бренд, цены
2. **Инвентарь** (`inventory`): Остатки, минимальные/максимальные запасы
3. **Продажи** (`sales`): История продаж с датами и количествами

### Примеры файлов
Примеры файлов находятся в папке `examples/`:
- `sample_products.csv` - Пример продуктов
- `sample_inventory.csv` - Пример инвентаря  
- `sample_sales.csv` - Пример продаж

## 🔌 API Endpoints

### Основные разделы
- **`/api/v1/data/`** - Загрузка и управление файлами
- **`/api/v1/inventory/`** - Управление инвентарем
- **`/api/v1/forecasts/`** - Прогнозирование спроса
- **`/api/v1/analytics/`** - Аналитика и отчеты

### Документация API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠️ Разработка

### Установка для разработки
```bash
make dev-setup
```

### Полезные команды
```bash
make help              # Показать все команды
make test              # Запуск тестов
make test-cov          # Тесты с покрытием
make lint              # Проверка кода
make format            # Форматирование кода
make clean             # Очистка временных файлов
make db-init           # Инициализация БД
make db-reset          # Сброс БД
```

### Структура backend
```
src/ainventory/
├── api/                    # FastAPI приложение
│   ├── main.py            # Основной сервер
│   ├── routers/           # API роутеры
│   └── schemas.py         # Pydantic схемы
├── database/              # База данных
│   ├── models.py          # SQLAlchemy модели
│   ├── connection.py      # Подключение к БД
│   └── init_db.py         # Инициализация БД
├── services/              # Бизнес-логика
│   └── file_processor.py  # Обработка файлов
└── forecasting/           # ML модели
    └── prophet_model.py   # Prophet интеграция
```

## 🔧 Конфигурация

### Переменные окружения
Скопируйте `env.example` в `.env` и настройте:

```bash
# База данных
DATABASE_URL=postgresql://ainventory:ainventory@localhost:5432/ainventory

# API настройки
API_HOST=0.0.0.0
API_PORT=8000

# Настройки файлов
UPLOAD_DIR=uploads
MAX_FILE_SIZE=52428800
```

### Настройка базы данных
```bash
# Создание базы данных
createdb ainventory

# Инициализация таблиц
make db-init
```

## 📈 Прогнозирование

### Поддерживаемые модели
- **Prophet** (Facebook) - для временных рядов
- **SARIMA** - для сезонных данных
- **Custom ML** - для специфических случаев

### Требования к данным
- Минимум 10 записей о продажах
- Временные ряды с регулярными интервалами
- Качественные данные без выбросов

## 🧪 Тестирование

### Запуск тестов
```bash
# Все тесты
make test

# С покрытием
make test-cov

# Конкретный тест
pytest tests/test_forecasting.py -v
```

### Примеры тестовых данных
Используйте файлы из папки `examples/` для тестирования API.

## 🔒 Безопасность

- Валидация всех входных данных
- Ограничение размера файлов
- Проверка типов файлов
- Логирование операций
- CORS настройки

## 📊 Мониторинг

### Статус сервисов
```bash
make status
```

### Логи
```bash
# Docker логи
make docker-logs

# Backend логи
tail -f logs/backend.log
```

## 🚀 Production

### Запуск в production
```bash
make prod-run
```

### Рекомендации
- Используйте reverse proxy (Nginx)
- Настройте SSL/TLS
- Настройте мониторинг
- Регулярные бэкапы БД
- Логирование и алерты

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📚 Документация

- [Backend API](src/ainventory/README.md) - Детальная документация API
- [Frontend](frontend/README.md) - Документация frontend
- [Архитектура](docs/architecture.md) - Описание архитектуры
- [API Reference](http://localhost:8000/docs) - Интерактивная документация API

## 🆘 Поддержка

### Частые проблемы
1. **Ошибка подключения к БД**: Проверьте `DATABASE_URL` и статус PostgreSQL
2. **Файл не загружается**: Проверьте формат и размер файла
3. **API не отвечает**: Проверьте статус backend сервиса

### Логи и отладка
```bash
# Логи backend
make docker-logs backend

# Проверка статуса
make status

# Тест API
curl http://localhost:8000/health
```

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🙏 Благодарности

- [FastAPI](https://fastapi.tiangolo.com/) - Современный Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [Prophet](https://facebook.github.io/prophet/) - Facebook's forecasting tool
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM
- [PostgreSQL](https://www.postgresql.org/) - Надежная СУБД
