# 🚀 Быстрый старт AInventory

## ⚡ За 5 минут

### 1. Установка зависимостей
```bash
# Python зависимости
pip install -r requirements.txt

# Node.js зависимости
cd frontend && npm install && cd ..
```

### 2. Настройка базы данных
```bash
# Создание базы данных
createdb ainventory

# Инициализация таблиц
python init_database.py
```

### 3. Запуск системы
```bash
# Запуск backend API
python run_backend.py

# В новом терминале - запуск frontend
cd frontend && npm run dev
```

### 4. Доступ к системе
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🐳 Docker (альтернатива)

```bash
# Сборка и запуск
make docker-build
make docker-run

# Просмотр логов
make docker-logs
```

## 📊 Тестирование

### Загрузка тестовых данных
```bash
# Тестирование API
python test_api.py
```

### Примеры файлов
- `examples/sample_products.csv` - Продукты
- `examples/sample_inventory.csv` - Инвентарь
- `examples/sample_sales.csv` - Продажи

## 🔧 Полезные команды

```bash
make help              # Все команды
make setup             # Полная настройка
make run               # Запуск всех сервисов
make status            # Статус сервисов
make clean             # Очистка
```

## 🆘 Проблемы

### Backend не запускается
```bash
# Проверка зависимостей
pip list | grep fastapi

# Проверка БД
python init_database.py
```

### Frontend не запускается
```bash
# Переустановка зависимостей
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### База данных недоступна
```bash
# Проверка PostgreSQL
sudo systemctl status postgresql

# Создание БД
sudo -u postgres createdb ainventory
```

## 📚 Документация

- [Полный README](README.md)
- [Backend API](src/ainventory/README.md)
- [API Reference](http://localhost:8000/docs)

## 🎯 Что дальше?

1. **Загрузите данные** через веб-интерфейс
2. **Изучите API** в Swagger UI
3. **Настройте прогнозирование** для ваших товаров
4. **Создайте отчеты** по инвентарю и продажам

---

**Вопросы?** Создайте Issue в репозитории или обратитесь к документации.
