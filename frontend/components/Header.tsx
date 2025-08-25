'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Menu, 
  X, 
  Bell, 
  User, 
  ChevronDown,
  Building2,
  Settings
} from 'lucide-react'

interface HeaderProps {
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
}

export default function Header({ sidebarOpen, setSidebarOpen }: HeaderProps) {
  const [warehouseOpen, setWarehouseOpen] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const [currentWarehouse, setCurrentWarehouse] = useState({ id: 1, name: 'Основной склад', location: 'Москва' })

  const warehouses = [
    { id: 1, name: 'Основной склад', location: 'Москва' },
    { id: 2, name: 'Склад №2', location: 'Санкт-Петербург' },
    { id: 3, name: 'Региональный склад', location: 'Екатеринбург' }
  ]

  const handleWarehouseChange = (warehouse: any) => {
    setCurrentWarehouse(warehouse)
    setWarehouseOpen(false)
    console.log('Выбран склад:', warehouse.name)
    // Здесь можно добавить обновление данных для выбранного склада
  }

  const handleNotifications = () => {
    console.log('Открыть уведомления')
    alert('У вас нет новых уведомлений!')
  }

  return (
    <header className="sticky top-0 z-40 bg-white border-b border-gray-200">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Mobile menu button */}
        <button
          type="button"
          className="lg:hidden -m-2.5 p-2.5 text-gray-700"
          onClick={() => setSidebarOpen(true)}
        >
          <span className="sr-only">Открыть меню</span>
          <Menu className="h-6 w-6" />
        </button>

        {/* Logo */}
        <div className="flex items-center">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center space-x-2"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">A</span>
            </div>
            <span className="text-xl font-bold text-gradient">AInventory</span>
          </motion.div>
        </div>

        {/* Right side */}
        <div className="flex items-center space-x-4">
          {/* Warehouse selector */}
          <div className="relative">
            <button
              onClick={() => setWarehouseOpen(!warehouseOpen)}
              className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition-colors duration-200"
            >
              <Building2 className="h-4 w-4" />
              <span>{currentWarehouse.name}</span>
              <ChevronDown className="h-4 w-4" />
            </button>

            {warehouseOpen && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50"
              >
                {warehouses.map((warehouse) => (
                  <button
                    key={warehouse.id}
                    className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200"
                    onClick={() => handleWarehouseChange(warehouse)}
                  >
                    <div className="font-medium">{warehouse.name}</div>
                    <div className="text-xs text-gray-500">{warehouse.location}</div>
                  </button>
                ))}
              </motion.div>
            )}
          </div>

          {/* Notifications */}
          <button 
            onClick={() => handleNotifications()} 
            className="p-2 text-gray-400 hover:text-gray-500 transition-colors duration-200 cursor-pointer"
          >
            <Bell className="h-5 w-5" />
          </button>

          {/* Profile */}
          <div className="relative">
            <button
              onClick={() => setProfileOpen(!profileOpen)}
              className="flex items-center space-x-2 p-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors duration-200"
            >
              <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <User className="h-4 w-4 text-primary-600" />
              </div>
              <ChevronDown className="h-4 w-4" />
            </button>

            {profileOpen && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50"
              >
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200">
                  <div className="flex items-center space-x-2">
                    <User className="h-4 w-4" />
                    <span>Профиль</span>
                  </div>
                </button>
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200">
                  <div className="flex items-center space-x-2">
                    <Settings className="h-4 w-4" />
                    <span>Настройки</span>
                  </div>
                </button>
                <div className="border-t border-gray-200 my-1"></div>
                <button className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors duration-200">
                  Выйти
                </button>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
