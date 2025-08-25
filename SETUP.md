# 🚀 Инструкция по настройке и запуску AInventory

## 📋 Предварительные требования

### Системные требования
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **RAM**: Минимум 8GB, рекомендуется 16GB+
- **Storage**: Минимум 5GB свободного места
- **Network**: Стабильное интернет-соединение

### Установленные программы
- **Node.js**: Версия 18.0.0 или выше
- **Python**: Версия 3.8 или выше
- **Docker**: Версия 20.10 или выше
- **Docker Compose**: Версия 2.0 или выше
- **Git**: Любая актуальная версия

### Проверка установки
```bash
# Проверка Node.js
node --version
npm --version

# Проверка Python
python --version
pip --version

# Проверка Docker
docker --version
docker-compose --version

# Проверка Git
git --version
```

## 🛠️ Установка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd ainventory_project
```

### 2. Настройка переменных окружения
Создайте файл `.env.local` в папке `frontend`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=AInventory
NODE_ENV=development
```

### 3. Установка зависимостей

#### Frontend зависимости
```bash
cd frontend
npm install
cd ..
```

#### Backend зависимости
```bash
# Создание виртуального окружения (рекомендуется)
python -m venv .venv

# Активация виртуального окружения
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

## 🚀 Запуск

### Вариант 1: Режим разработки (рекомендуется для разработчиков)

#### Запуск фронтенда
```bash
cd frontend
npm run dev
```
Фронтенд будет доступен по адресу: http://localhost:3000

#### Запуск backend
```bash
# В новом терминале
python -m uvicorn src.ainventory.main:app --reload --host 0.0.0.0 --port 8000
```
Backend API будет доступен по адресу: http://localhost:8000

#### Запуск базы данных (опционально)
```bash
# PostgreSQL
docker run -d --name ainventory-db -e POSTGRES_DB=ainventory -e POSTGRES_USER=ainventory -e POSTGRES_PASSWORD=ainventory -p 5432:5432 postgres:15

# Redis
docker run -d --name ainventory-redis -p 6379:6379 redis:7-alpine
```

### Вариант 2: Docker Compose (рекомендуется для продакшена)

#### Первоначальная настройка
```bash
# Сборка образов
make build

# Запуск всех сервисов
make up
```

#### Управление сервисами
```bash
# Просмотр статуса
make status

# Просмотр логов
make logs

# Перезапуск
make restart

# Остановка
make down

# Полная очистка
make clean
```

### Вариант 3: Make команды (упрощенный)

```bash
# Первоначальная настройка
make setup

# Запуск в режиме разработки
make dev

# Запуск в продакшн режиме
make prod
```

## 🌐 Доступ к приложению

После успешного запуска:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **База данных**: localhost:5432
- **Redis**: localhost:6379

## 🔧 Настройка

### Настройка базы данных
1. Подключитесь к PostgreSQL
2. Создайте базу данных `ainventory`
3. Примените миграции (если есть)

### Настройка ML моделей
1. Убедитесь, что установлены все Python зависимости
2. Проверьте доступность ML библиотек (Prophet, LightGBM, etc.)
3. Настройте параметры моделей в конфигурации

### Настройка уведомлений
1. Создайте Telegram бота (опционально)
2. Настройте SMTP для email уведомлений
3. Настройте webhook для push уведомлений

## 🧪 Тестирование

### Frontend тесты
```bash
cd frontend
npm run test
npm run lint
npm run build
```

### Backend тесты
```bash
# Запуск тестов
pytest tests/ -v

# Проверка качества кода
flake8 src/ tests/
black --check .
isort --check-only .
```

### E2E тесты (если настроены)
```bash
npm run test:e2e
```

## 📊 Мониторинг

### Логи приложения
```bash
# Docker логи
docker-compose logs -f

# Frontend логи
cd frontend && npm run dev

# Backend логи
# Логи будут в терминале при запуске uvicorn
```

### Метрики производительности
- **Frontend**: Chrome DevTools Performance
- **Backend**: FastAPI встроенные метрики
- **Database**: PostgreSQL статистика

## 🚨 Устранение неполадок

### Частые проблемы

#### 1. Порт 3000 занят
```bash
# Найти процесс
netstat -ano | findstr :3000
# Windows
taskkill /PID <PID> /F
# macOS/Linux
kill -9 <PID>
```

#### 2. Порт 8000 занят
```bash
# Найти процесс
netstat -ano | findstr :8000
# Остановить процесс аналогично
```

#### 3. Проблемы с Docker
```bash
# Перезапуск Docker
docker system prune -f
docker-compose down -v
docker-compose up -d
```

#### 4. Проблемы с зависимостями
```bash
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Backend
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

#### 5. Проблемы с базой данных
```bash
# Перезапуск PostgreSQL
docker restart ainventory-db

# Проверка подключения
docker exec -it ainventory-db psql -U ainventory -d ainventory
```

### Логи ошибок

#### Frontend ошибки
- Проверьте консоль браузера (F12)
- Проверьте терминал с `npm run dev`
- Проверьте файл `.next/server/error.log`

#### Backend ошибки
- Проверьте терминал с uvicorn
- Проверьте логи Docker контейнера
- Проверьте системные логи

## 🔒 Безопасность

### Переменные окружения
- Никогда не коммитьте `.env` файлы
- Используйте разные ключи для dev/prod
- Регулярно обновляйте секретные ключи

### Доступ к базе данных
- Измените пароли по умолчанию
- Ограничьте доступ к портам БД
- Используйте SSL соединения в продакшене

### API безопасность
- Настройте CORS политики
- Используйте rate limiting
- Настройте аутентификацию

## 📈 Масштабирование

### Горизонтальное масштабирование
```bash
# Масштабирование frontend
docker-compose up -d --scale frontend=3

# Масштабирование backend
docker-compose up -d --scale backend=3
```

### Вертикальное масштабирование
- Увеличьте RAM для Docker
- Настройте swap файлы
- Оптимизируйте настройки БД

## 🚀 Развертывание в продакшене

### Подготовка
1. Настройте продакшн переменные окружения
2. Настройте SSL сертификаты
3. Настройте мониторинг и логирование
4. Настройте backup стратегию

### Развертывание
```bash
# Продакшн сборка
make full-build

# Запуск
make prod

# Проверка статуса
make status
```

### Мониторинг
- Настройте алерты
- Настройте метрики
- Настройте логирование

## 📚 Дополнительные ресурсы

- [Frontend документация](frontend/README.md)
- [API документация](http://localhost:8000/docs)
- [Архитектура проекта](docs/architecture.md)
- [ML модели](docs/adr/ADR-0001-adopt-prophet-vs-sarima.md)

## 🤝 Поддержка

Если у вас возникли проблемы:

1. Проверьте раздел "Устранение неполадок"
2. Посмотрите существующие issues
3. Создайте новый issue с подробным описанием
4. Обратитесь в поддержку: support@ainventory.com

## 🎉 Готово!

Поздравляем! Вы успешно настроили и запустили AInventory. 

Теперь вы можете:
- Открыть приложение в браузере
- Изучить API документацию
- Начать работу с данными
- Настраивать ML модели
- Разрабатывать новые функции

Удачи в использовании AInventory! 🚀
