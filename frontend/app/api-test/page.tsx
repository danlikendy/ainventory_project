'use client'

import { useState } from 'react'

export default function ApiTest() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const testEndpoint = async (endpoint: string, params: Record<string, string> = {}) => {
    setLoading(true)
    setError(null)
    
    try {
      const url = new URL(endpoint, window.location.origin)
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.append(key, value)
      })
      
      const response = await fetch(url)
      const result = await response.json()
      
      if (response.ok) {
        setData(result)
      } else {
        setError(result.error || 'Ошибка запроса')
      }
    } catch (err: any) {
      setError(err.message || 'Неизвестная ошибка')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">API Тестирование</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* GET endpoints */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900">GET Endpoints</h2>
            
            <div className="space-y-2">
              <button
                onClick={() => testEndpoint('/api/data')}
                className="w-full btn-primary text-left"
                disabled={loading}
              >
                Все данные
              </button>
              
              <button
                onClick={() => testEndpoint('/api/data', { type: 'sales' })}
                className="w-full btn-secondary text-left"
                disabled={loading}
              >
                Только продажи
              </button>
              
              <button
                onClick={() => testEndpoint('/api/data', { type: 'inventory' })}
                className="w-full btn-secondary text-left"
                disabled={loading}
              >
                Только инвентарь
              </button>
              
              <button
                onClick={() => testEndpoint('/api/data', { type: 'forecasts' })}
                className="w-full btn-secondary text-left"
                disabled={loading}
              >
                Только прогнозы
              </button>
              
              <button
                onClick={() => testEndpoint('/api/data', { warehouse: 'Москва' })}
                className="w-full btn-secondary text-left"
                disabled={loading}
              >
                Фильтр по складу (Москва)
              </button>
            </div>
          </div>
          
          {/* POST endpoints */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900">POST Endpoints</h2>
            
            <div className="space-y-2">
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-800">
                  <strong>Загрузка файлов:</strong><br/>
                  POST /api/upload<br/>
                  Content-Type: multipart/form-data<br/>
                  Body: file (Excel/CSV)
                </p>
              </div>
              
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm text-green-800">
                  <strong>Обновление данных:</strong><br/>
                  POST /api/data<br/>
                  Body: action: updateInventory, data: {...}
                </p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Результат */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900">Результат</h2>
          
          {loading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="text-gray-600 mt-2">Загрузка...</p>
            </div>
          )}
          
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800 font-medium">Ошибка:</p>
              <p className="text-red-700">{error}</p>
            </div>
          )}
          
          {data && (
            <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                <h3 className="font-medium text-gray-900">Ответ API</h3>
              </div>
              <div className="p-4">
                <pre className="text-sm text-gray-800 overflow-auto max-h-96">
                  {JSON.stringify(data, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
        
        {/* Документация API */}
        <div className="mt-8 p-6 bg-gray-100 rounded-lg">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Документация API</h2>
          
          <div className="space-y-4 text-sm text-gray-700">
            <div>
              <h3 className="font-medium text-gray-900">GET /api/data</h3>
              <p>Получить данные о продажах, инвентаре и прогнозах</p>
              <p><strong>Параметры:</strong></p>
              <ul className="list-disc list-inside ml-4 space-y-1">
                <li><code>type</code> - тип данных (sales, inventory, forecasts)</li>
                <li><code>warehouse</code> - фильтр по складу</li>
                <li><code>category</code> - фильтр по категории</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900">POST /api/data</h3>
              <p>Обновить данные</p>
              <p><strong>Body:</strong></p>
              <ul className="list-disc list-inside ml-4 space-y-1">
                <li><code>action</code> - действие (updateInventory, addSales)</li>
                <li><code>data</code> - данные для обновления</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900">POST /api/upload</h3>
              <p>Загрузить Excel/CSV файл с данными</p>
              <p><strong>Body:</strong> multipart/form-data с полем file</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
