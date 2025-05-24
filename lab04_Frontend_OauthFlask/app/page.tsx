"use client"

import { useAuth } from "@/contexts/auth-context"
import { LoginForm } from "@/components/login-form"
import { Dashboard } from "@/components/dashboard"

export default function Home() {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">Sistema de Gestión de Biblioteca</h2>
            <p className="mt-2 text-center text-sm text-gray-600">Inicia sesión para acceder al sistema</p>
          </div>
          <LoginForm />
        </div>
      </div>
    )
  }

  return <Dashboard />
}
