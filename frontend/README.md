# AInventory Frontend

Современное веб-приложение для прогнозирования спроса и управления запасами, построенное на React + Next.js.

## 🚀 Быстрый старт

### Предварительные требования

- Node.js 18+ 
- npm или yarn

### Установка

1. Установите зависимости:
```bash
npm install
# или
yarn install
```

2. Запустите приложение в режиме разработки:
```bash
npm run dev
# или
yarn dev
```

3. Откройте [http://localhost:3000](http://localhost:3000) в браузере

## 🛠️ Технологии

- **Framework**: Next.js 14
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Forms**: React Hook Form
- **Notifications**: React Hot Toast

## 📁 Структура проекта

```
frontend/
├── app/                    # Next.js App Router
│   ├── globals.css        # Глобальные стили
│   ├── layout.tsx         # Корневой layout
│   └── page.tsx           # Главная страница
├── components/            # React компоненты
│   ├── Dashboard.tsx      # Главный дашборд
│   ├── Header.tsx         # Верхняя панель
│   └── Sidebar.tsx        # Боковая навигация
├── public/                # Статические файлы
└── package.json           # Зависимости
```

## 🎨 Компоненты

### Dashboard
- Карточки с ключевыми метриками
- График прогноза спроса
- Круговая диаграмма категорий
- Таблица анализа SKU

### Header
- Логотип AInventory
- Выбор склада/филиала
- Уведомления
- Профиль пользователя

### Sidebar
- Навигация по разделам
- Адаптивное меню для мобильных устройств
- Дополнительные ссылки

## 🔧 Настройка

### Переменные окружения
Создайте файл `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=AInventory
```

### Tailwind CSS
Настройки в `tailwind.config.js` включают:
- Кастомные цвета для брендинга
- Анимации и переходы
- Адаптивные breakpoints

## 📱 Адаптивность

Приложение полностью адаптивно и работает на:
- 🖥️ Desktop (1024px+)
- 📱 Tablet (768px - 1023px)
- 📱 Mobile (до 767px)

## 🚀 Сборка для продакшена

```bash
npm run build
npm start
```

## 🔗 Интеграция с Backend

Приложение готово к интеграции с FastAPI backend через:
- REST API endpoints
- WebSocket для real-time обновлений
- JWT аутентификация

## 📊 Возможности

- ✅ Современный UI/UX дизайн
- ✅ Интерактивные графики и диаграммы
- ✅ Адаптивная верстка
- ✅ Анимации и переходы
- ✅ Готовность к монетизации
- ✅ TypeScript поддержка
- ✅ SEO оптимизация

## 🎯 Следующие шаги

1. Интеграция с ML моделями
2. Реализация аутентификации
3. Добавление Telegram бота
4. Интеграция с Excel API
5. Мультискладовость
6. Система подписок
