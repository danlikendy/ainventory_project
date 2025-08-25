import { NextRequest, NextResponse } from 'next/server'
import { readFile, readdir } from 'fs/promises'
import { join } from 'path'

// Временные данные - в реальности будут из базы данных
const mockRealData = {
  sales: [
    { date: '2024-01-01', sku: 'SKU001', quantity: 45, revenue: 22500, warehouse: 'Москва' },
    { date: '2024-01-02', sku: 'SKU001', quantity: 52, revenue: 26000, warehouse: 'Москва' },
    { date: '2024-01-03', sku: 'SKU002', quantity: 38, revenue: 19000, warehouse: 'СПб' },
    { date: '2024-01-04', sku: 'SKU003', quantity: 67, revenue: 33500, warehouse: 'Москва' },
    { date: '2024-01-05', sku: 'SKU001', quantity: 41, revenue: 20500, warehouse: 'СПб' },
  ],
  inventory: [
    { sku: 'SKU001', name: 'iPhone 15 Pro', stock: 156, minStock: 50, maxStock: 200, warehouse: 'Москва', category: 'Электроника', brand: 'Apple' },
    { sku: 'SKU002', name: 'MacBook Air M2', stock: 23, minStock: 20, maxStock: 100, warehouse: 'СПб', category: 'Электроника', brand: 'Apple' },
    { sku: 'SKU003', name: 'Nike Air Max', stock: 89, minStock: 30, maxStock: 150, warehouse: 'Москва', category: 'Обувь', brand: 'Nike' },
    { sku: 'SKU004', name: 'Adidas Ultraboost', stock: 45, minStock: 25, maxStock: 80, warehouse: 'СПб', category: 'Обувь', brand: 'Adidas' },
    { sku: 'SKU005', name: 'Samsung Galaxy S24', stock: 67, minStock: 40, maxStock: 120, warehouse: 'Москва', category: 'Электроника', brand: 'Samsung' },
  ],
  forecasts: [
    { sku: 'SKU001', date: '2024-02-01', forecast: 180, confidence: 0.85, model: 'Prophet' },
    { sku: 'SKU002', date: '2024-02-01', forecast: 45, confidence: 0.78, model: 'SARIMA' },
    { sku: 'SKU003', date: '2024-02-01', forecast: 120, confidence: 0.92, model: 'LightGBM' },
    { sku: 'SKU004', date: '2024-02-01', forecast: 65, confidence: 0.81, model: 'Prophet' },
    { sku: 'SKU005', date: '2024-02-01', forecast: 95, confidence: 0.88, model: 'Ensemble' },
  ]
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const type = searchParams.get('type') || 'all'
    const warehouse = searchParams.get('warehouse')
    const category = searchParams.get('category')
    
    let data = mockRealData
    
    // Фильтрация по складу
    if (warehouse) {
      data.sales = data.sales.filter(item => item.warehouse === warehouse)
      data.inventory = data.inventory.filter(item => item.warehouse === warehouse)
    }
    
    // Фильтрация по категории
    if (category) {
      data.inventory = data.inventory.filter(item => item.category === category)
    }
    
    // Возвращаем только нужный тип данных
    if (type === 'sales') {
      return NextResponse.json({ data: data.sales })
    } else if (type === 'inventory') {
      return NextResponse.json({ data: data.inventory })
    } else if (type === 'forecasts') {
      return NextResponse.json({ data: data.forecasts })
    }
    
    return NextResponse.json({ data })
    
  } catch (error) {
    console.error('Ошибка получения данных:', error)
    return NextResponse.json(
      { error: 'Ошибка получения данных' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { action, data } = body
    
    switch (action) {
      case 'updateInventory':
        // В реальности здесь будет обновление базы данных
        return NextResponse.json({ message: 'Инвентарь обновлен', data })
        
      case 'addSales':
        // В реальности здесь будет добавление продаж
        return NextResponse.json({ message: 'Продажи добавлены', data })
        
      default:
        return NextResponse.json(
          { error: 'Неизвестное действие' },
          { status: 400 }
        )
    }
    
  } catch (error) {
    console.error('Ошибка обработки данных:', error)
    return NextResponse.json(
      { error: 'Ошибка обработки данных' },
      { status: 500 }
    )
  }
}
