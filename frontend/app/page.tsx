'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  Package, 
  BarChart3, 
  Settings as SettingsIcon, 
  Bell, 
  Download,
  Upload,
  Users,
  Zap,
  Shield,
  CheckCircle,
  Star
} from 'lucide-react'
import Dashboard from '@/components/Dashboard'
import Forecasts from '@/components/Forecasts'
import Inventory from '@/components/Inventory'
import Reports from '@/components/Reports'
import Settings from '@/components/Settings'
import DataUpload from '@/components/DataUpload'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [currentView, setCurrentView] = useState('dashboard')

  const views = {
    dashboard: <Dashboard />,
    forecasts: <Forecasts />,
    inventory: <Inventory />,
    reports: <Reports />,
    settings: <Settings />,
    data: <DataUpload />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} currentView={currentView} setCurrentView={setCurrentView} />
      
      <div className="lg:pl-72">
        <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
        
        <main className="py-8">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            {views[currentView as keyof typeof views]}
          </div>
        </main>
      </div>
    </div>
  )
}
