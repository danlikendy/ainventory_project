'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Settings as SettingsIcon, 
  User, 
  Bell, 
  Shield, 
  Database,
  Zap,
  Globe,
  Palette,
  Save,
  Eye,
  EyeOff,
  Key,
  Trash2
} from 'lucide-react'

const settingSections = [
  { id: 'profile', name: 'Профиль', icon: User, description: 'Личные данные и настройки аккаунта' },
  { id: 'notifications', name: 'Уведомления', icon: Bell, description: 'Настройки уведомлений и алертов' },
  { id: 'security', name: 'Безопасность', icon: Shield, description: 'Пароли и настройки безопасности' },
  { id: 'integrations', name: 'Интеграции', icon: Zap, description: 'API ключи и внешние сервисы' },
  { id: 'data', name: 'Данные', icon: Database, description: 'Управление данными и экспорт' },
  { id: 'appearance', name: 'Внешний вид', icon: Palette, description: 'Темы и настройки интерфейса' },
]

export default function Settings() {
  const [activeSection, setActiveSection] = useState('profile')
  const [showPassword, setShowPassword] = useState(false)
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    telegram: false,
    lowStock: true,
    forecastUpdates: true,
    systemAlerts: false,
  })

  const renderProfileSettings = () => (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center">
          <User className="h-10 w-10 text-primary-600" />
        </div>
        <div>
          <h3 className="text-lg font-medium text-gray-900">Фото профиля</h3>
          <p className="text-sm text-gray-500">JPG, PNG или GIF. Максимум 2MB.</p>
          <button className="mt-2 btn-secondary">Изменить фото</button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Имя</label>
          <input type="text" className="input-field" defaultValue="Иван" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Фамилия</label>
          <input type="text" className="input-field" defaultValue="Иванов" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
          <input type="email" className="input-field" defaultValue="ivan@example.com" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Телефон</label>
          <input type="tel" className="input-field" defaultValue="+7 (999) 123-45-67" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Компания</label>
          <input type="text" className="input-field" defaultValue="ООО Рога и Копыта" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Должность</label>
          <input type="text" className="input-field" defaultValue="Менеджер по закупкам" />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">О себе</label>
        <textarea 
          rows={3} 
          className="input-field"
          defaultValue="Менеджер по закупкам с опытом работы в сфере управления запасами более 5 лет."
        />
      </div>
    </div>
  )

  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Каналы уведомлений</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Globe className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <div className="font-medium text-gray-900">Email уведомления</div>
                <div className="text-sm text-gray-500">Получать уведомления на email</div>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                className="sr-only peer"
                checked={notifications.email}
                onChange={(e) => setNotifications({...notifications, email: e.target.checked})}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <Bell className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <div className="font-medium text-gray-900">Push уведомления</div>
                <div className="text-sm text-gray-500">Уведомления в браузере</div>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                className="sr-only peer"
                checked={notifications.push}
                onChange={(e) => setNotifications({...notifications, push: e.target.checked})}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                <Zap className="h-5 w-5 text-white" />
              </div>
              <div>
                <div className="font-medium text-gray-900">Telegram уведомления</div>
                <div className="text-sm text-gray-500">Уведомления в Telegram</div>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                className="sr-only peer"
                checked={notifications.telegram}
                onChange={(e) => setNotifications({...notifications, telegram: e.target.checked})}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Типы уведомлений</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="font-medium text-gray-900">Низкий уровень запасов</div>
              <div className="text-sm text-gray-500">Уведомления о критически низких остатках</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                className="sr-only peer"
                checked={notifications.lowStock}
                onChange={(e) => setNotifications({...notifications, lowStock: e.target.checked})}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <div className="font-medium text-gray-900">Обновления прогнозов</div>
              <div className="text-sm text-gray-500">Уведомления о новых прогнозах спроса</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                className="sr-only peer"
                checked={notifications.forecastUpdates}
                onChange={(e) => setNotifications({...notifications, forecastUpdates: e.target.checked})}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <div className="font-medium text-gray-900">Системные уведомления</div>
              <div className="text-sm text-gray-500">Технические уведомления и обновления</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                className="sr-only peer"
                checked={notifications.systemAlerts}
                onChange={(e) => setNotifications({...notifications, systemAlerts: e.target.checked})}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>
        </div>
      </div>
    </div>
  )

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Смена пароля</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Текущий пароль</label>
            <div className="relative">
              <input 
                type={showPassword ? "text" : "password"} 
                className="input-field pr-10"
                placeholder="Введите текущий пароль"
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5 text-gray-400" />
                ) : (
                  <Eye className="h-5 w-5 text-gray-400" />
                )}
              </button>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Новый пароль</label>
            <input 
              type="password" 
              className="input-field"
              placeholder="Введите новый пароль"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Подтвердите новый пароль</label>
            <input 
              type="password" 
              className="input-field"
              placeholder="Повторите новый пароль"
            />
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Двухфакторная аутентификация</h3>
        <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
          <div>
            <div className="font-medium text-gray-900">2FA защита</div>
            <div className="text-sm text-gray-500">Дополнительный уровень безопасности для вашего аккаунта</div>
          </div>
          <button className="btn-primary">Настроить 2FA</button>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Сессии</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
            <div>
              <div className="font-medium text-gray-900">Текущая сессия</div>
              <div className="text-sm text-gray-500">Windows 10 • Chrome • Москва</div>
            </div>
            <span className="text-sm text-green-600 font-medium">Активна</span>
          </div>
          
          <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
            <div>
              <div className="font-medium text-gray-900">Другая сессия</div>
              <div className="text-sm text-gray-500">iPhone • Safari • Санкт-Петербург</div>
            </div>
            <button className="text-sm text-red-600 hover:text-red-800">Завершить</button>
          </div>
        </div>
      </div>
    </div>
  )

  const renderIntegrationsSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">API ключи</h3>
        <div className="space-y-4">
          <div className="p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium text-gray-900">Основной API ключ</span>
              <button className="text-sm text-blue-600 hover:text-blue-800">Обновить</button>
            </div>
            <div className="flex items-center space-x-2">
              <input 
                type="password" 
                value="sk_live_1234567890abcdef" 
                readOnly
                className="input-field font-mono text-sm"
              />
              <button className="btn-secondary">Копировать</button>
            </div>
            <p className="text-xs text-gray-500 mt-1">Создан: 15 января 2024 • Последнее использование: 2 часа назад</p>
          </div>
          
          <button className="btn-primary flex items-center space-x-2">
            <Key className="h-4 w-4" />
            <span>Создать новый API ключ</span>
          </button>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Внешние сервисы</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                <Zap className="h-5 w-5 text-white" />
              </div>
              <div>
                <div className="font-medium text-gray-900">Telegram Bot</div>
                <div className="text-sm text-gray-500">Уведомления и отчеты в Telegram</div>
              </div>
            </div>
            <button className="btn-secondary">Настроить</button>
          </div>
          
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
                <Database className="h-5 w-5 text-white" />
              </div>
              <div>
                <div className="font-medium text-gray-900">Excel Export</div>
                <div className="text-sm text-gray-500">Автоматический экспорт данных в Excel</div>
              </div>
            </div>
            <button className="btn-secondary">Настроить</button>
          </div>
        </div>
      </div>
    </div>
  )

  const renderDataSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Экспорт данных</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button className="p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <Database className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <div className="font-medium text-gray-900">Экспорт в Excel</div>
                <div className="text-sm text-gray-500">Все данные в формате .xlsx</div>
              </div>
            </div>
          </button>
          
          <button className="p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Zap className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <div className="font-medium text-gray-900">Экспорт в CSV</div>
                <div className="text-sm text-gray-500">Данные в текстовом формате</div>
              </div>
            </div>
          </button>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Резервное копирование</h3>
        <div className="p-4 border border-gray-200 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="font-medium text-gray-900">Автоматическое резервное копирование</div>
              <div className="text-sm text-gray-500">Создание резервных копий каждые 24 часа</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" defaultChecked />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>
          
          <div className="flex items-center space-x-4">
            <button className="btn-primary">Создать резервную копию</button>
            <button className="btn-secondary">Восстановить из копии</button>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Удаление данных</h3>
        <div className="p-4 border border-red-200 rounded-lg bg-red-50">
          <div className="flex items-center space-x-3 mb-3">
            <Trash2 className="h-5 w-5 text-red-600" />
            <span className="font-medium text-red-900">Опасная зона</span>
          </div>
          <p className="text-sm text-red-700 mb-4">
            Удаление аккаунта приведет к безвозвратной потере всех данных. 
            Это действие нельзя отменить.
          </p>
          <button className="btn-secondary border-red-300 text-red-700 hover:bg-red-100">
            Удалить аккаунт
          </button>
        </div>
      </div>
    </div>
  )

  const renderAppearanceSettings = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Тема оформления</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="p-4 border-2 border-primary-500 rounded-lg bg-primary-50">
            <div className="w-full h-20 bg-white rounded-lg mb-3 border-2 border-gray-200"></div>
            <div className="text-center">
              <div className="font-medium text-primary-900">Светлая</div>
              <div className="text-sm text-primary-700">По умолчанию</div>
            </div>
          </button>
          
          <button className="p-4 border-2 border-gray-200 rounded-lg hover:border-gray-300">
            <div className="w-full h-20 bg-gray-800 rounded-lg mb-3 border-2 border-gray-200"></div>
            <div className="text-center">
              <div className="font-medium text-gray-900">Темная</div>
              <div className="text-sm text-gray-600">Комфортно для глаз</div>
            </div>
          </button>
          
          <button className="p-4 border-2 border-gray-200 rounded-lg hover:border-gray-300">
            <div className="w-full h-20 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg mb-3 border-2 border-gray-200"></div>
            <div className="text-center">
              <div className="font-medium text-gray-900">Авто</div>
              <div className="text-sm text-gray-600">По системным настройкам</div>
            </div>
          </button>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Язык интерфейса</h3>
        <select className="input-field w-64">
          <option value="ru">Русский</option>
          <option value="en">English</option>
          <option value="de">Deutsch</option>
          <option value="fr">Français</option>
        </select>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Часовой пояс</h3>
        <select className="input-field w-64">
          <option value="Europe/Moscow">Москва (UTC+3)</option>
          <option value="Europe/London">Лондон (UTC+0)</option>
          <option value="America/New_York">Нью-Йорк (UTC-5)</option>
          <option value="Asia/Tokyo">Токио (UTC+9)</option>
        </select>
      </div>
    </div>
  )

  const renderSectionContent = () => {
    switch (activeSection) {
      case 'profile':
        return renderProfileSettings()
      case 'notifications':
        return renderNotificationSettings()
      case 'security':
        return renderSecuritySettings()
      case 'integrations':
        return renderIntegrationsSettings()
      case 'data':
        return renderDataSettings()
      case 'appearance':
        return renderAppearanceSettings()
      default:
        return renderProfileSettings()
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Настройки</h1>
        <p className="text-gray-600">Управление профилем, безопасностью и настройками приложения</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <nav className="space-y-2">
            {settingSections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`w-full text-left p-4 rounded-lg transition-colors ${
                  activeSection === section.id
                    ? 'bg-primary-50 text-primary-900 border border-primary-200'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <section.icon className={`h-5 w-5 ${
                    activeSection === section.id ? 'text-primary-600' : 'text-gray-500'
                  }`} />
                  <div>
                    <div className="font-medium">{section.name}</div>
                    <div className="text-sm text-gray-500">{section.description}</div>
                  </div>
                </div>
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="lg:col-span-3">
          <motion.div
            key={activeSection}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
            className="card"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                {settingSections.find(s => s.id === activeSection)?.name}
              </h2>
              <button className="btn-primary flex items-center space-x-2">
                <Save className="h-4 w-4" />
                <span>Сохранить</span>
              </button>
            </div>
            
            {renderSectionContent()}
          </motion.div>
        </div>
      </div>
    </div>
  )
}
