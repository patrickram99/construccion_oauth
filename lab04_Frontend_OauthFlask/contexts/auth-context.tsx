"use client"

import type React from "react"
import { createContext, useContext, useState, useEffect } from "react"

interface AuthContextType {
  token: string | null
  isAuthenticated: boolean
  login: (clientId: string, clientSecret: string) => Promise<boolean>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const savedToken = localStorage.getItem("auth_token")
    if (savedToken) {
      setToken(savedToken)
    }
    setIsLoading(false)
  }, [])

  const login = async (clientId: string, clientSecret: string): Promise<boolean> => {
    try {
      const response = await fetch("http://localhost:5000/api/auth/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          client_id: clientId,
          client_secret: clientSecret,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        const authToken = data.token_acceso
        setToken(authToken)
        localStorage.setItem("auth_token", authToken)
        return true
      }
      return false
    } catch (error) {
      console.error("Error de autenticación:", error)
      return false
    }
  }

  const logout = () => {
    setToken(null)
    localStorage.removeItem("auth_token")
  }

  return (
    <AuthContext.Provider
      value={{
        token,
        isAuthenticated: !!token,
        login,
        logout,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth debe ser usado dentro de un AuthProvider")
  }
  return context
}
