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
	@echo "Установка Python зависимостей..."
	$(PIP) install -r requirements.txt
	@echo "Установка Node.js зависимостей..."
	cd $(FRONTEND_DIR) && npm install

run-backend: ## Запустить backend API
	@echo "Запуск Backend API..."
	cd $(BACKEND_DIR)/api && $(PYTHON) -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

run-frontend: ## Запустить frontend
	@echo "Запуск Frontend..."
	cd $(FRONTEND_DIR) && npm run dev

run: ## Запустить все сервисы
	@echo "Запуск всех сервисов..."
	@echo "Backend будет доступен на http://localhost:8000"
	@echo "Frontend будет доступен на http://localhost:3000"
	@echo "Документация API: http://localhost:8000/docs"
	@echo ""
	@echo "Нажмите Ctrl+C для остановки"
	@make -j2 run-backend run-frontend

test: ## Запустить тесты
	@echo "Запуск тестов..."
	$(PYTHON) -m pytest tests/ -v

lint: ## Проверить код линтером
	@echo "Проверка кода..."
	$(PYTHON) -m black --check $(BACKEND_DIR)
	$(PYTHON) -m isort --check-only $(BACKEND_DIR)
	$(PYTHON) -m flake8 $(BACKEND_DIR)

format: ## Форматировать код
	@echo "Форматирование кода..."
	$(PYTHON) -m black $(BACKEND_DIR)
	$(PYTHON) -m isort $(BACKEND_DIR)

clean: ## Очистить временные файлы
	@echo "Очистка временных файлов..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-build: ## Собрать Docker образы
	@echo "Сборка Docker образов..."
	docker-compose build

docker-run: ## Запустить сервисы в Docker
	@echo "Запуск сервисов в Docker..."
	docker-compose up -d

docker-stop: ## Остановить Docker сервисы
	@echo "Остановка Docker сервисов..."
	docker-compose down

docker-logs: ## Показать логи Docker сервисов
	@echo "Логи Docker сервисов..."
	docker-compose logs -f

setup: ## Полная настройка проекта
	@echo "Полная настройка проекта..."
	@make install
