.PHONY: help install run test clean docker-build docker-run docker-stop

# Переменные
PYTHON = python3
PIP = pip3
BACKEND_DIR = src/ainventory
FRONTEND_DIR = frontend

help: ## Показать справку
	@echo "AInventory - Система управления инвентарем и прогнозирования спроса"
	@echo ""
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "📦 Установка Python зависимостей..."
	$(PIP) install -r requirements.txt
	@echo "📦 Установка Node.js зависимостей..."
	cd $(FRONTEND_DIR) && npm install

install-dev: ## Установить зависимости для разработки
	@echo "📦 Установка Python зависимостей для разработки..."
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	@echo "📦 Установка Node.js зависимостей..."
	cd $(FRONTEND_DIR) && npm install

run-backend: ## Запустить backend API
	@echo "🚀 Запуск Backend API..."
	$(PYTHON) run_backend.py

run-frontend: ## Запустить frontend
	@echo "🚀 Запуск Frontend..."
	cd $(FRONTEND_DIR) && npm run dev

run: ## Запустить все сервисы
	@echo "🚀 Запуск всех сервисов..."
	@echo "Backend будет доступен на http://localhost:8000"
	@echo "Frontend будет доступен на http://localhost:3000"
	@echo "Документация API: http://localhost:8000/docs"
	@echo ""
	@echo "Нажмите Ctrl+C для остановки"
	@make -j2 run-backend run-frontend

test: ## Запустить тесты
	@echo "🧪 Запуск тестов..."
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Запустить тесты с покрытием
	@echo "🧪 Запуск тестов с покрытием..."
	$(PYTHON) -m pytest tests/ --cov=$(BACKEND_DIR) --cov-report=html

lint: ## Проверить код линтером
	@echo "🔍 Проверка кода..."
	$(PYTHON) -m black --check $(BACKEND_DIR)
	$(PYTHON) -m isort --check-only $(BACKEND_DIR)
	$(PYTHON) -m flake8 $(BACKEND_DIR)

format: ## Форматировать код
	@echo "✨ Форматирование кода..."
	$(PYTHON) -m black $(BACKEND_DIR)
	$(PYTHON) -m isort $(BACKEND_DIR)

clean: ## Очистить временные файлы
	@echo "🧹 Очистка временных файлов..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-build: ## Собрать Docker образы
	@echo "🐳 Сборка Docker образов..."
	docker-compose build

docker-run: ## Запустить сервисы в Docker
	@echo "🐳 Запуск сервисов в Docker..."
	docker-compose up -d

docker-stop: ## Остановить Docker сервисы
	@echo "🐳 Остановка Docker сервисов..."
	docker-compose down

docker-logs: ## Показать логи Docker сервисов
	@echo "📋 Логи Docker сервисов..."
	docker-compose logs -f

db-init: ## Инициализировать базу данных
	@echo "🗄️ Инициализация базы данных..."
	$(PYTHON) -c "from src.ainventory.database.init_db import init_db; import asyncio; asyncio.run(init_db())"

db-reset: ## Сбросить базу данных
	@echo "🗄️ Сброс базы данных..."
	$(PYTHON) -c "from src.ainventory.database.init_db import reset_db; reset_db()"

setup: ## Полная настройка проекта
	@echo "🔧 Полная настройка проекта..."
	@make install
	@make db-init
	@echo "✅ Настройка завершена!"

dev-setup: ## Настройка для разработки
	@echo "🔧 Настройка для разработки..."
	@make install-dev
	@make db-init
	@echo "✅ Настройка для разработки завершена!"

# Команды для разработки
watch: ## Запустить в режиме наблюдения
	@echo "👀 Запуск в режиме наблюдения..."
	$(PYTHON) -m uvicorn $(BACKEND_DIR).api.main:app --reload --host 0.0.0.0 --port 8000

# Команды для production
prod-run: ## Запуск в production режиме
	@echo "🚀 Запуск в production режиме..."
	$(PYTHON) -m uvicorn $(BACKEND_DIR).api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Команды для миграций
migrate: ## Создать миграцию
	@echo "🔄 Создание миграции..."
	alembic revision --autogenerate -m "$(message)"

migrate-up: ## Применить миграции
	@echo "🔄 Применение миграций..."
	alembic upgrade head

migrate-down: ## Откатить миграции
	@echo "🔄 Откат миграций..."
	alembic downgrade -1

# Команды для мониторинга
status: ## Показать статус сервисов
	@echo "📊 Статус сервисов..."
	@echo "Backend API:"
	@curl -s http://localhost:8000/health || echo "❌ Не запущен"
	@echo "Frontend:"
	@curl -s http://localhost:3000 > /dev/null && echo "✅ Работает" || echo "❌ Не запущен"

# Команды для документации
docs: ## Сгенерировать документацию
	@echo "📚 Генерация документации..."
	$(PYTHON) -m pdoc --html $(BACKEND_DIR) --output-dir docs/api

# Команды для безопасности
security-check: ## Проверить безопасность
	@echo "🔒 Проверка безопасности..."
	$(PIP) install safety
	$(PYTHON) -m safety check

# Команды для бэкапа
backup: ## Создать бэкап базы данных
	@echo "💾 Создание бэкапа базы данных..."
	@echo "Используйте: pg_dump -h localhost -U ainventory -d ainventory > backup_$(shell date +%Y%m%d_%H%M%S).sql"

restore: ## Восстановить базу данных из бэкапа
	@echo "💾 Восстановление базы данных..."
	@echo "Используйте: psql -h localhost -U ainventory -d ainventory < backup_file.sql"
