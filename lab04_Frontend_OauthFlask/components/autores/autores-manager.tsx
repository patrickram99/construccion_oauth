"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/contexts/auth-context"
import { useToast } from "@/hooks/use-toast"
import { apiService, type Autor } from "@/services/api"
import { AutorForm } from "./autor-form"
import { AutorList } from "./autor-list"
import { Plus } from "lucide-react"

export function AutoresManager() {
  const [autores, setAutores] = useState<Autor[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingAutor, setEditingAutor] = useState<Autor | null>(null)
  const { token } = useAuth()
  const { toast } = useToast()

  useEffect(() => {
    loadAutores()
  }, [])

  const loadAutores = async () => {
    if (!token) return

    try {
      setIsLoading(true)
      const data = await apiService.getAutores(token)
      setAutores(data)
    } catch (error) {
      toast({
        title: "Error",
        description: "Error al cargar los autores",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingAutor(null)
    setShowForm(true)
  }

  const handleEdit = (autor: Autor) => {
    setEditingAutor(autor)
    setShowForm(true)
  }

  const handleSave = async (autorData: Autor) => {
    if (!token) return

    try {
      if (editingAutor?.id) {
        await apiService.updateAutor(token, editingAutor.id, autorData)
        toast({
          title: "Éxito",
          description: "Autor actualizado correctamente",
        })
      } else {
        await apiService.createAutor(token, autorData)
        toast({
          title: "Éxito",
          description: "Autor creado correctamente",
        })
      }
      setShowForm(false)
      setEditingAutor(null)
      loadAutores()
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Error al guardar el autor",
        variant: "destructive",
      })
    }
  }

  const handleDelete = async (id: number) => {
    if (!token) return

    try {
      await apiService.deleteAutor(token, id)
      toast({
        title: "Éxito",
        description: "Autor eliminado correctamente",
      })
      loadAutores()
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Error al eliminar el autor",
        variant: "destructive",
      })
    }
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingAutor(null)
  }

  if (showForm) {
    return <AutorForm autor={editingAutor} onSave={handleSave} onCancel={handleCancel} />
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>Gestión de Autores</CardTitle>
          <Button onClick={handleCreate}>
            <Plus className="mr-2 h-4 w-4" />
            Nuevo Autor
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <AutorList autores={autores} isLoading={isLoading} onEdit={handleEdit} onDelete={handleDelete} />
      </CardContent>
    </Card>
  )
}
