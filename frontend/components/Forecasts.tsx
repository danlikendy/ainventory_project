'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  Calendar, 
  Download, 
  Upload,
  Play,
  Pause,
  RefreshCw,
  BarChart3,
  Settings,
  AlertTriangle
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts'

const historicalData = [
  { date: '2024-01-01', sales: 120, seasonality: 1.1, promotion: 0 },
  { date: '2024-01-02', sales: 135, seasonality: 1.1, promotion: 0 },
  { date: '2024-01-03', sales: 110, seasonality: 1.1, promotion: 0 },
  { date: '2024-01-04', sales: 125, seasonality: 1.1, promotion: 0 },
  { date: '2024-01-05', sales: 140, seasonality: 1.1, promotion: 0 },
  { date: '2024-01-06', sales: 130, seasonality: 1.1, promotion: 0 },
  { date: '2024-01-07', sales: 115, seasonality: 1.1, promotion: 0 },
]

const forecastData = [
  { date: '2024-02-01', forecast: 125, upper: 140, lower: 110, confidence: 0.85 },
  { date: '2024-02-02', forecast: 130, upper: 145, lower: 115, confidence: 0.83 },
  { date: '2024-02-03', forecast: 135, upper: 150, lower: 120, confidence: 0.81 },
  { date: '2024-02-04', forecast: 140, upper: 155, lower: 125, confidence: 0.79 },
  { date: '2024-02-05', forecast: 145, upper: 160, lower: 130, confidence: 0.77 },
  { date: '2024-02-06', forecast: 150, upper: 165, lower: 135, confidence: 0.75 },
  { date: '2024-02-07', forecast: 155, upper: 170, lower: 140, confidence: 0.73 },
]

const modelMetrics = [
  { name: 'Prophet', mape: 12.5, rmse: 15.2, accuracy: 87.5, status: 'active' },
  { name: 'SARIMA', mape: 14.2, rmse: 18.1, accuracy: 85.8, status: 'active' },
  { name: 'LightGBM', mape: 11.8, rmse: 14.5, accuracy: 88.2, status: 'training' },
  { name: 'Ensemble', mape: 10.1, rmse: 13.2, accuracy: 89.9, status: 'active' },
]

export default function Forecasts() {
  const [selectedModel, setSelectedModel] = useState('ensemble')
  const [forecastPeriod, setForecastPeriod] = useState(30)
  const [isTraining, setIsTraining] = useState(false)

  const handleModelTraining = () => {
    setIsTraining(true)
    // Симуляция обучения модели
    setTimeout(() => setIsTraining(false), 3000)
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Прогнозирование спроса</h1>
          <p className="text-gray-600">ML-модели для прогнозирования спроса с доверительными интервалами</p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="btn-secondary flex items-center space-x-2">
            <Upload className="h-4 w-4" />
            <span>Загрузить данные</span>
          </button>
          <button className="btn-primary flex items-center space-x-2">
            <Download className="h-4 w-4" />
            <span>Экспорт прогноза</span>
          </button>
        </div>
      </div>

      {/* Model Selection & Training */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Model Selection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Выбор модели</h3>
          <div className="space-y-3">
            {modelMetrics.map((model) => (
              <div
                key={model.name}
                className={`p-3 rounded-lg border-2 cursor-pointer transition-all ${
                  selectedModel === model.name.toLowerCase()
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => setSelectedModel(model.name.toLowerCase())}
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-900">{model.name}</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    model.status === 'active' ? 'bg-green-100 text-green-800' :
                    model.status === 'training' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {model.status === 'active' ? 'Активна' :
                     model.status === 'training' ? 'Обучение' : 'Неактивна'}
                  </span>
                </div>
                <div className="mt-2 text-sm text-gray-600">
                  <div>MAPE: {model.mape}%</div>
                  <div>RMSE: {model.rmse}</div>
                  <div>Точность: {model.accuracy}%</div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Training Controls */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Управление моделями</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Период прогноза (дни)
              </label>
              <input
                type="number"
                value={forecastPeriod}
                onChange={(e) => setForecastPeriod(Number(e.target.value))}
                className="input-field"
                min="7"
                max="365"
              />
            </div>
            
            <button
              onClick={handleModelTraining}
              disabled={isTraining}
              className={`w-full btn-primary flex items-center justify-center space-x-2 ${
                isTraining ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {isTraining ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  <span>Обучение...</span>
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  <span>Обучить модель</span>
                </>
              )}
            </button>

            <button className="w-full btn-secondary flex items-center justify-center space-x-2">
              <Settings className="h-4 w-4" />
              <span>Настройки модели</span>
            </button>
          </div>
        </motion.div>

        {/* Forecast Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Сводка прогноза</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <span className="text-sm font-medium text-blue-900">Период прогноза</span>
              <span className="text-lg font-bold text-blue-900">{forecastPeriod} дней</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <span className="text-sm font-medium text-green-900">Средний спрос</span>
              <span className="text-lg font-bold text-green-900">142 ед/день</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <span className="text-sm font-medium text-yellow-900">Доверие</span>
              <span className="text-lg font-bold text-yellow-900">85%</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
              <span className="text-sm font-medium text-red-900">Риск дефицита</span>
              <span className="text-lg font-bold text-red-900">12 SKU</span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Historical vs Forecast */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Исторические данные vs Прогноз</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={[...historicalData, ...forecastData]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Area 
                type="monotone" 
                dataKey="sales" 
                stroke="#3B82F6" 
                fill="#3B82F6" 
                fillOpacity={0.3}
                name="Исторические продажи"
              />
              <Area 
                type="monotone" 
                dataKey="forecast" 
                stroke="#10B981" 
                fill="#10B981" 
                fillOpacity={0.3}
                name="Прогноз"
              />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Confidence Intervals */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Доверительные интервалы</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={forecastData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="forecast" 
                stroke="#3B82F6" 
                strokeWidth={2}
                name="Прогноз"
              />
              <Line 
                type="monotone" 
                dataKey="upper" 
                stroke="#EF4444" 
                strokeWidth={1}
                strokeDasharray="5 5"
                name="Верхняя граница"
              />
              <Line 
                type="monotone" 
                dataKey="lower" 
                stroke="#EF4444" 
                strokeWidth={1}
                strokeDasharray="5 5"
                name="Нижняя граница"
              />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Anomalies & Insights */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.5 }}
        className="card"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Аномалии и инсайты</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3 flex items-center">
              <AlertTriangle className="h-5 w-5 text-yellow-500 mr-2" />
              Обнаруженные аномалии
            </h4>
            <div className="space-y-2">
              <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                <div className="text-sm font-medium text-yellow-800">Пик спроса 15 января</div>
                <div className="text-xs text-yellow-600">Продажи выросли на 45% без промо</div>
              </div>
              <div className="p-3 bg-red-50 rounded-lg border border-red-200">
                <div className="text-sm font-medium text-red-800">Падение спроса 22 января</div>
                <div className="text-xs text-red-600">Продажи упали на 30%</div>
              </div>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3 flex items-center">
              <BarChart3 className="h-5 w-5 text-blue-500 mr-2" />
              Сезонные паттерны
            </h4>
            <div className="space-y-2">
              <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                <div className="text-sm font-medium text-blue-800">Понедельник - пик</div>
                <div className="text-xs text-blue-600">+25% от среднего</div>
              </div>
              <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                <div className="text-sm font-medium text-green-800">Воскресенье - спад</div>
                <div className="text-xs text-green-600">-15% от среднего</div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
