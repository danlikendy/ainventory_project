'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, FileText, AlertCircle, CheckCircle, X } from 'lucide-react'
import toast from 'react-hot-toast'

interface UploadStatus {
  fileName: string
  status: 'uploading' | 'success' | 'error'
  message: string
}

export default function DataUpload() {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<UploadStatus[]>([])
  const [isProcessing, setIsProcessing] = useState(false)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const files = Array.from(e.dataTransfer.files)
    await uploadFiles(files)
  }

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    await uploadFiles(files)
  }

  const uploadFiles = async (files: File[]) => {
    setIsProcessing(true)
    
    for (const file of files) {
      const status: UploadStatus = {
        fileName: file.name,
        status: 'uploading',
        message: 'Загрузка...'
      }
      
      setUploadStatus(prev => [...prev, status])
      
      try {
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        })
        
        if (response.ok) {
          const result = await response.json()
          setUploadStatus(prev => 
            prev.map(item => 
              item.fileName === file.name 
                ? { ...item, status: 'success', message: 'Успешно загружен' }
                : item
            )
          )
          toast.success(`${file.name} успешно загружен`)
        } else {
          const error = await response.json()
          setUploadStatus(prev => 
            prev.map(item => 
              item.fileName === file.name 
                ? { ...item, status: 'error', message: error.error || 'Ошибка загрузки' }
                : item
            )
          )
          toast.error(`Ошибка загрузки ${file.name}`)
        }
      } catch (error) {
        setUploadStatus(prev => 
          prev.map(item => 
            item.fileName === file.name 
              ? { ...item, status: 'error', message: 'Ошибка сети' }
              : item
          )
        )
        toast.error(`Ошибка сети при загрузке ${file.name}`)
      }
    }
    
    setIsProcessing(false)
  }

  const removeStatus = (fileName: string) => {
    setUploadStatus(prev => prev.filter(item => item.fileName !== fileName))
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">Загрузка данных</h2>
        <p className="text-gray-600">Загрузите Excel или CSV файлы с вашими данными</p>
      </div>

      {/* Drag & Drop Zone */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <Upload className="mx-auto h-12 w-12 text-gray-400" />
        <div className="mt-4">
          <p className="text-lg font-medium text-gray-900">
            Перетащите файлы сюда или
          </p>
          <label className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 cursor-pointer">
            <input
              type="file"
              multiple
              accept=".xlsx,.xls,.csv"
              onChange={handleFileSelect}
              className="hidden"
            />
            Выберите файлы
          </label>
        </div>
        <p className="mt-2 text-sm text-gray-500">
          Поддерживаются файлы Excel (.xlsx, .xls) и CSV
        </p>
      </div>

      {/* Upload Status */}
      {uploadStatus.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-lg font-medium text-gray-900">Статус загрузки</h3>
          {uploadStatus.map((status, index) => (
            <motion.div
              key={status.fileName}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                {status.status === 'uploading' && (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600" />
                )}
                {status.status === 'success' && (
                  <CheckCircle className="h-5 w-5 text-green-600" />
                )}
                {status.status === 'error' && (
                  <AlertCircle className="h-5 w-5 text-red-600" />
                )}
                <FileText className="h-5 w-5 text-gray-400" />
                <span className="font-medium text-gray-900">{status.fileName}</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`text-sm ${
                  status.status === 'success' ? 'text-green-600' :
                  status.status === 'error' ? 'text-red-600' :
                  'text-blue-600'
                }`}>
                  {status.message}
                </span>
                <button
                  onClick={() => removeStatus(status.fileName)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">Формат данных</h4>
        <div className="text-sm text-blue-800 space-y-1">
          <p>• <strong>Продажи:</strong> Дата, SKU, Количество, Выручка, Склад</p>
          <p>• <strong>Инвентарь:</strong> SKU, Название, Остаток, Мин. остаток, Макс. остаток, Склад, Категория, Бренд</p>
          <p>• <strong>Прогнозы:</strong> SKU, Дата, Прогноз, Уверенность, Модель</p>
        </div>
      </div>
    </div>
  )
}
