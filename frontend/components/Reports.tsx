'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  FileText, 
  Download, 
  Calendar,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Package,
  Users,
  BarChart3,
  PieChart,
  LineChart,
  Filter
} from 'lucide-react'
import { LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart as RechartsPieChart, Pie, Cell, AreaChart, Area } from 'recharts'

const salesData = [
  { month: 'Янв', sales: 125000, profit: 31250, units: 1250 },
  { month: 'Фев', sales: 135000, profit: 33750, units: 1350 },
  { month: 'Мар', sales: 140000, profit: 35000, units: 1400 },
  { month: 'Апр', sales: 130000, profit: 32500, units: 1300 },
  { month: 'Май', sales: 145000, profit: 36250, units: 1450 },
  { month: 'Июн', sales: 150000, profit: 37500, units: 1500 },
]

const topProducts = [
  { name: 'Товар A', sales: 25000, units: 250, margin: 25, growth: 12 },
  { name: 'Товар B', sales: 22000, units: 220, margin: 18, growth: 8 },
  { name: 'Товар C', sales: 20000, units: 200, margin: 32, growth: 15 },
  { name: 'Товар D', sales: 18000, units: 180, margin: 15, growth: -5 },
  { name: 'Товар E', sales: 16000, units: 160, margin: 28, growth: 20 },
]

const categoryPerformance = [
  { name: 'Электроника', sales: 45, profit: 28, growth: 15 },
  { name: 'Одежда', sales: 25, profit: 18, growth: 8 },
  { name: 'Книги', sales: 20, profit: 32, growth: 12 },
  { name: 'Спорт', sales: 10, profit: 22, growth: 25 },
]

const reportTypes = [
  { id: 'sales', name: 'Отчет по продажам', icon: TrendingUp, description: 'Анализ продаж по периодам и категориям' },
  { id: 'inventory', name: 'Отчет по запасам', icon: Package, description: 'Состояние запасов и оборот товаров' },
  { id: 'profitability', name: 'Отчет по прибыльности', icon: DollarSign, description: 'Анализ маржи и рентабельности' },
  { id: 'customers', name: 'Отчет по клиентам', icon: Users, description: 'Поведение и сегментация клиентов' },
]

export default function Reports() {
  const [selectedReport, setSelectedReport] = useState('sales')
  const [dateRange, setDateRange] = useState('month')
  const [selectedCategory, setSelectedCategory] = useState('all')

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0,
    }).format(value)
  }

  const formatNumber = (value: number) => {
    return new Intl.NumberFormat('ru-RU').format(value)
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Отчеты и аналитика</h1>
          <p className="text-gray-600">Детальная аналитика продаж, запасов и прибыльности</p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="btn-secondary flex items-center space-x-2">
            <Filter className="h-4 w-4" />
            <span>Фильтры</span>
          </button>
          <button className="btn-primary flex items-center space-x-2">
            <Download className="h-4 w-4" />
            <span>Экспорт отчета</span>
          </button>
        </div>
      </div>

      {/* Report Type Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {reportTypes.map((report) => (
          <motion.div
            key={report.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: report.id === 'sales' ? 0 : report.id === 'inventory' ? 0.1 : report.id === 'profitability' ? 0.2 : 0.3 }}
            className={`card cursor-pointer transition-all ${
              selectedReport === report.id ? 'ring-2 ring-primary-500 bg-primary-50' : 'hover:shadow-md'
            }`}
            onClick={() => setSelectedReport(report.id)}
          >
            <div className="flex items-center space-x-3">
              <div className={`p-3 rounded-lg ${
                selectedReport === report.id ? 'bg-primary-100' : 'bg-gray-100'
              }`}>
                <report.icon className={`h-6 w-6 ${
                  selectedReport === report.id ? 'text-primary-600' : 'text-gray-600'
                }`} />
              </div>
              <div>
                <h3 className={`font-medium ${
                  selectedReport === report.id ? 'text-primary-900' : 'text-gray-900'
                }`}>
                  {report.name}
                </h3>
                <p className="text-sm text-gray-600">{report.description}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex items-center space-x-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Период</label>
            <select 
              value={dateRange} 
              onChange={(e) => setDateRange(e.target.value)}
              className="input-field w-40"
            >
              <option value="week">Неделя</option>
              <option value="month">Месяц</option>
              <option value="quarter">Квартал</option>
              <option value="year">Год</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Категория</label>
            <select 
              value={selectedCategory} 
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="input-field w-40"
            >
              <option value="all">Все категории</option>
              <option value="Электроника">Электроника</option>
              <option value="Одежда">Одежда</option>
              <option value="Книги">Книги</option>
              <option value="Спорт">Спорт</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Дата начала</label>
            <input 
              type="date" 
              className="input-field w-40"
              defaultValue="2024-01-01"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Дата окончания</label>
            <input 
              type="date" 
              className="input-field w-40"
              defaultValue="2024-06-30"
            />
          </div>
        </div>
      </div>

      {/* Sales Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Общие продажи</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <span className="text-sm font-medium text-blue-900">Объем продаж</span>
              <span className="text-lg font-bold text-blue-900">{formatCurrency(825000)}</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <span className="text-sm font-medium text-green-900">Прибыль</span>
              <span className="text-lg font-bold text-green-900">{formatCurrency(206250)}</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <span className="text-sm font-medium text-purple-900">Единиц продано</span>
              <span className="text-lg font-bold text-purple-900">{formatNumber(8250)}</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <span className="text-sm font-medium text-yellow-900">Средняя маржа</span>
              <span className="text-lg font-bold text-yellow-900">25%</span>
            </div>
          </div>
        </motion.div>

        {/* Sales Trend Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="card lg:col-span-2"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Тренд продаж</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={salesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [
                  name === 'sales' ? formatCurrency(value as number) : 
                  name === 'profit' ? formatCurrency(value as number) : 
                  formatNumber(value as number),
                  name === 'sales' ? 'Продажи' : 
                  name === 'profit' ? 'Прибыль' : 'Единицы'
                ]}
              />
              <Area 
                type="monotone" 
                dataKey="sales" 
                stroke="#3B82F6" 
                fill="#3B82F6" 
                fillOpacity={0.3}
                name="sales"
              />
              <Area 
                type="monotone" 
                dataKey="profit" 
                stroke="#10B981" 
                fill="#10B981" 
                fillOpacity={0.3}
                name="profit"
              />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Top Products & Category Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Products */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Топ товары по продажам</h3>
          <div className="space-y-4">
            {topProducts.map((product, index) => (
              <div key={product.name} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <span className="text-sm font-bold text-primary-600">{index + 1}</span>
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">{product.name}</div>
                    <div className="text-sm text-gray-600">{formatCurrency(product.sales)}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-gray-900">{formatNumber(product.units)} ед.</div>
                  <div className={`text-xs font-medium ${
                    product.growth > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {product.growth > 0 ? '+' : ''}{product.growth}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Category Performance */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.7 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Производительность категорий</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoryPerformance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="sales" fill="#3B82F6" name="Продажи %" />
              <Bar dataKey="profit" fill="#10B981" name="Прибыль %" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Detailed Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.8 }}
        className="card"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Детальные метрики</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
            <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <TrendingUp className="h-6 w-6 text-white" />
            </div>
            <div className="text-2xl font-bold text-blue-900">+15.2%</div>
            <div className="text-sm text-blue-700">Рост продаж</div>
          </div>
          
          <div className="text-center p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
            <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <DollarSign className="h-6 w-6 text-white" />
            </div>
            <div className="text-2xl font-bold text-green-900">25.0%</div>
            <div className="text-sm text-green-700">Средняя маржа</div>
          </div>
          
          <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
            <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <Package className="h-6 w-6 text-white" />
            </div>
            <div className="text-2xl font-bold text-purple-900">1,375</div>
            <div className="text-sm text-purple-700">Средний чек</div>
          </div>
          
          <div className="text-center p-4 bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg">
            <div className="w-12 h-12 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <Users className="h-6 w-6 text-white" />
            </div>
            <div className="text-2xl font-bold text-yellow-900">600</div>
            <div className="text-sm text-yellow-700">Активных клиентов</div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
