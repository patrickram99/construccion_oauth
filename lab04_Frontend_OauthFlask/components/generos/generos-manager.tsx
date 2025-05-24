"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/contexts/auth-context"
import { useToast } from "@/hooks/use-toast"
import { apiService, type Genero } from "@/services/api"
import { GeneroForm } from "./genero-form"
import { GeneroList } from "./genero-list"
import { Plus } from "lucide-react"

export function GenerosManager() {
  const [generos, setGeneros] = useState<Genero[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingGenero, setEditingGenero] = useState<Genero | null>(null)
  const { token } = useAuth()
  const { toast } = useToast()

  useEffect(() => {
    loadGeneros()
  }, [])

  const loadGeneros = async () => {
    if (!token) return

    try {
      setIsLoading(true)
      const data = await apiService.getGeneros(token)
      setGeneros(data)
    } catch (error) {
      toast({
        title: "Error",
        description: "Error al cargar los géneros",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingGenero(null)
    setShowForm(true)
  }

  const handleEdit = (genero: Genero) => {
    setEditingGenero(genero)
    setShowForm(true)
  }

  const handleSave = async (generoData: Genero) => {
    if (!token) return

    try {
      if (editingGenero?.id) {
        await apiService.updateGenero(token, editingGenero.id, generoData)
        toast({
          title: "Éxito",
          description: "Género actualizado correctamente",
        })
      } else {
        await apiService.createGenero(token, generoData)
        toast({
          title: "Éxito",
          description: "Género creado correctamente",
        })
      }
      setShowForm(false)
      setEditingGenero(null)
      loadGeneros()
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Error al guardar el género",
        variant: "destructive",
      })
    }
  }

  const handleDelete = async (id: number) => {
    if (!token) return

    try {
      await apiService.deleteGenero(token, id)
      toast({
        title: "Éxito",
        description: "Género eliminado correctamente",
      })
      loadGeneros()
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Error al eliminar el género",
        variant: "destructive",
      })
    }
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingGenero(null)
  }

  if (showForm) {
    return <GeneroForm genero={editingGenero} onSave={handleSave} onCancel={handleCancel} />
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>Gestión de Géneros</CardTitle>
          <Button onClick={handleCreate}>
            <Plus className="mr-2 h-4 w-4" />
            Nuevo Género
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <GeneroList generos={generos} isLoading={isLoading} onEdit={handleEdit} onDelete={handleDelete} />
      </CardContent>
    </Card>
  )
}
