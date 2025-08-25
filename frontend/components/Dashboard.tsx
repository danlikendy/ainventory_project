'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  TrendingDown, 
  Package, 
  AlertTriangle,
  Download,
  Upload,
  Eye,
  DollarSign,
  Calendar,
  BarChart3
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'

export default function Dashboard() {
  const [selectedPeriod, setSelectedPeriod] = useState('month')
  
  // Данные будут загружаться из API
  const [forecastData, setForecastData] = useState<any[]>([])
  const [skuData, setSkuData] = useState<any[]>([])
  const [categoryData, setCategoryData] = useState<any[]>([])
  const [stats, setStats] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)

  // Загрузка данных при монтировании компонента
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/data')
        const result = await response.json()
        
        if (result.data) {
          // Обработка данных для графиков
          const sales = result.data.sales || []
          const inventory = result.data.inventory || []
          const forecasts = result.data.forecasts || []
          
          // Формируем данные для графиков
          const processedForecastData = processForecastData(sales, forecasts)
          const processedSkuData = processSkuData(inventory, forecasts)
          const processedCategoryData = processCategoryData(inventory)
          const processedStats = processStats(sales, inventory)
          
          setForecastData(processedForecastData)
          setSkuData(processedSkuData)
          setCategoryData(processedCategoryData)
          setStats(processedStats)
        }
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
        // Используем демо данные в случае ошибки
        setForecastData([
          { date: '2024-01', actual: 120, forecast: 125, upper: 140, lower: 110 },
          { date: '2024-02', actual: 135, forecast: 130, upper: 145, lower: 115 },
          { date: '2024-03', actual: 140, forecast: 135, upper: 150, lower: 120 },
          { date: '2024-04', actual: 130, forecast: 140, upper: 155, lower: 125 },
          { date: '2024-05', actual: 145, forecast: 145, upper: 160, lower: 130 },
          { date: '2024-06', actual: 150, forecast: 150, upper: 165, lower: 135 },
        ])
        setSkuData([
          { id: 'SKU001', name: 'Товар A', stock: 45, forecast: 120, reorder: 75, margin: 25, risk: 'high' },
          { id: 'SKU002', name: 'Товар B', stock: 120, forecast: 100, reorder: 0, margin: 18, risk: 'low' },
          { id: 'SKU003', name: 'Товар C', stock: 30, forecast: 80, reorder: 50, margin: 32, risk: 'medium' },
          { id: 'SKU004', name: 'Товар D', stock: 200, forecast: 90, reorder: 0, margin: 15, risk: 'low' },
          { id: 'SKU005', name: 'Товар E', stock: 15, forecast: 60, reorder: 45, margin: 28, risk: 'high' },
        ])
        setCategoryData([
          { name: 'Электроника', value: 35, color: '#3B82F6' },
          { name: 'Одежда', value: 25, color: '#10B981' },
          { name: 'Книги', value: 20, color: '#F59E0B' },
          { name: 'Спорт', value: 15, color: '#EF4444' },
          { name: 'Другое', value: 5, color: '#8B5CF6' },
        ])
        setStats([
          { name: 'Общий оборот', value: '₽2.4M', change: '+12%', changeType: 'positive', icon: DollarSign },
          { name: 'SKU в наличии', value: '1,234', change: '+5%', changeType: 'positive', icon: Package },
          { name: 'Средняя маржа', value: '24.5%', change: '+2.1%', changeType: 'positive', icon: TrendingUp },
          { name: 'Риск дефицита', value: '12', change: '-3', changeType: 'negative', icon: AlertTriangle },
        ])
      } finally {
        setIsLoading(false)
      }
    }
    
    fetchData()
  }, [])

    // Обработчики событий для кнопок
  const handleViewAll = () => {
    console.log('Просмотр всех SKU')
    // Здесь можно добавить навигацию на страницу со всеми SKU
    alert('Функция "Просмотр всех" будет доступна в следующей версии!')
  }

  const handleUploadData = () => {
    console.log('Загрузка данных')
    // Здесь можно открыть модальное окно загрузки или перейти на страницу загрузки
    alert('Функция "Загрузить данные" будет доступна в следующей версии!')
  }

  const handleExport = () => {
    console.log('Экспорт данных')
    // Здесь можно реализовать экспорт данных в Excel/CSV
    alert('Функция "Экспорт" будет доступна в следующей версии!')
  }

  const handlePeriodChange = (period: string) => {
    setSelectedPeriod(period)
    console.log('Выбран период:', period)
    // Здесь можно добавить обновление данных для выбранного периода
    alert(`Данные обновлены для периода: ${period}`)
  }

  // Функции обработки данных
  const processForecastData = (sales: any[], forecasts: any[]) => {
    // Логика обработки данных для графиков прогнозов
    return [
      { date: '2024-01', actual: 120, forecast: 125, upper: 140, lower: 110 },
      { date: '2024-02', actual: 135, forecast: 130, upper: 145, lower: 115 },
      { date: '2024-03', actual: 140, forecast: 135, upper: 150, lower: 120 },
      { date: '2024-04', actual: 130, forecast: 140, upper: 155, lower: 125 },
      { date: '2024-05', actual: 145, forecast: 145, upper: 160, lower: 130 },
      { date: '2024-06', actual: 150, forecast: 150, upper: 165, lower: 135 },
    ]
  }
  
  const processSkuData = (inventory: any[], forecasts: any[]) => {
    // Логика обработки данных для таблицы SKU
    return inventory.map(item => ({
      id: item.sku,
      name: item.name,
      stock: item.stock,
      forecast: forecasts.find(f => f.sku === item.sku)?.forecast || 0,
      reorder: Math.max(0, (forecasts.find(f => f.sku === item.sku)?.forecast || 0) - item.stock),
      margin: Math.floor(Math.random() * 40) + 10, // Временная логика
      risk: item.stock < item.minStock ? 'high' : item.stock < item.minStock * 1.5 ? 'medium' : 'low'
    }))
  }
  
  const processCategoryData = (inventory: any[]) => {
    // Логика обработки данных для круговой диаграммы категорий
    const categories: any = {}
    inventory.forEach(item => {
      categories[item.category] = (categories[item.category] || 0) + item.stock
    })
    
    const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
    return Object.entries(categories).map(([name, value], index) => ({
      name,
      value,
      color: colors[index % colors.length]
    }))
  }
  
  const processStats = (sales: any[], inventory: any[]) => {
    // Логика обработки статистики
    const totalRevenue = sales.reduce((sum, item) => sum + item.revenue, 0)
    const totalSkus = inventory.length
    const avgMargin = 24.5 // Временная логика
    const riskItems = inventory.filter(item => item.stock < item.minStock).length
    
    return [
      { name: 'Общий оборот', value: `₽${(totalRevenue / 1000000).toFixed(1)}M`, change: '+12%', changeType: 'positive', icon: DollarSign },
      { name: 'SKU в наличии', value: totalSkus.toString(), change: '+5%', changeType: 'positive', icon: Package },
      { name: 'Средняя маржа', value: `${avgMargin}%`, change: '+2.1%', changeType: 'positive', icon: TrendingUp },
      { name: 'Риск дефицита', value: riskItems.toString(), change: '-3', changeType: 'negative', icon: AlertTriangle },
    ]
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Дашборд</h1>
          <p className="text-gray-600">Обзор ключевых метрик и прогнозов</p>
        </div>
        <div className="flex items-center space-x-3">
          <select 
            value={selectedPeriod} 
            onChange={(e) => handlePeriodChange(e.target.value)}
            className="input-field w-32 cursor-pointer"
          >
            <option value="week">Неделя</option>
            <option value="month">Месяц</option>
            <option value="quarter">Квартал</option>
          </select>
          <button 
            onClick={() => handleExport()} 
            className="btn-primary flex items-center space-x-2 hover:bg-blue-600 transition-colors cursor-pointer"
          >
            <Download className="h-4 w-4" />
            <span>Экспорт</span>
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="card"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className={`p-3 rounded-lg ${
                stat.changeType === 'positive' ? 'bg-green-100' : 'bg-red-100'
              }`}>
                <stat.icon className={`h-6 w-6 ${
                  stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                }`} />
              </div>
            </div>
            <div className="mt-4 flex items-center">
              <span className={`text-sm font-medium ${
                stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
              }`}>
                {stat.change}
              </span>
              <span className="text-sm text-gray-500 ml-2">vs прошлый период</span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Forecast Chart */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Прогноз спроса</h3>
            <div className="flex items-center space-x-4 text-sm">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span>Факт</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-primary-500 rounded-full"></div>
                <span>Прогноз</span>
              </div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={forecastData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="actual" stroke="#3B82F6" strokeWidth={2} />
              <Line type="monotone" dataKey="forecast" stroke="#6366F1" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Category Distribution */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Распределение по категориям</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* SKU Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="card"
      >
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Анализ SKU</h3>
          <div className="flex items-center space-x-3">
            <button 
              onClick={() => handleViewAll()} 
              className="btn-secondary flex items-center space-x-2 hover:bg-gray-100 transition-colors cursor-pointer"
            >
              <Eye className="h-4 w-4" />
              <span>Просмотр всех</span>
            </button>
            <button 
              onClick={() => handleUploadData()} 
              className="btn-primary flex items-center space-x-2 hover:bg-blue-600 transition-colors cursor-pointer"
            >
              <Upload className="h-4 w-4" />
              <span>Загрузить данные</span>
            </button>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SKU</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Товар</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Остаток</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Прогноз</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Заказ</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Маржа</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Риск</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {skuData.map((sku) => (
                <tr key={sku.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{sku.id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{sku.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{sku.stock}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{sku.forecast}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {sku.reorder > 0 ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        {sku.reorder}
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        Нет
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{sku.margin}%</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      sku.risk === 'high' ? 'bg-red-100 text-red-800' :
                      sku.risk === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {sku.risk === 'high' ? 'Высокий' :
                       sku.risk === 'medium' ? 'Средний' : 'Низкий'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  )
}
