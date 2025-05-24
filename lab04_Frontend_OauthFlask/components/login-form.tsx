"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/contexts/auth-context"
import { useToast } from "@/hooks/use-toast"
import { Loader2 } from "lucide-react"

export function LoginForm() {
  const [clientId, setClientId] = useState("test_client")
  const [clientSecret, setClientSecret] = useState("test_secret")
  const [isLoading, setIsLoading] = useState(false)
  const { login } = useAuth()
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const success = await login(clientId, clientSecret)
      if (success) {
        toast({
          title: "Éxito",
          description: "Sesión iniciada correctamente",
        })
      } else {
        toast({
          title: "Error",
          description: "Credenciales inválidas",
          variant: "destructive",
        })
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Error de conexión con el servidor",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Iniciar Sesión</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="clientId">ID del Cliente</Label>
            <Input id="clientId" type="text" value={clientId} onChange={(e) => setClientId(e.target.value)} required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="clientSecret">Secreto del Cliente</Label>
            <Input
              id="clientSecret"
              type="password"
              value={clientSecret}
              onChange={(e) => setClientSecret(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Iniciar Sesión
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
