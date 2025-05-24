"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/contexts/auth-context"
import { useToast } from "@/hooks/use-toast"
import { apiService, type Libro, type Autor, type Genero } from "@/services/api"
import { LibroForm } from "./libro-form"
import { LibroList } from "./libro-list"
import { Plus, Search } from "lucide-react"
import { LibrosPorFiltro } from "./libros-por-filtro"

export function LibrosManager() {
  const [libros, setLibros] = useState<Libro[]>([])
  const [autores, setAutores] = useState<Autor[]>([])
  const [generos, setGeneros] = useState<Genero[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingLibro, setEditingLibro] = useState<Libro | null>(null)
  const { token } = useAuth()
  const { toast } = useToast()
  const [showFiltros, setShowFiltros] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    if (!token) return

    try {
      setIsLoading(true)
      const [librosData, autoresData, generosData] = await Promise.all([
        apiService.getLibros(token),
        apiService.getAutores(token),
        apiService.getGeneros(token),
      ])
      setLibros(librosData)
      setAutores(autoresData)
      setGeneros(generosData)
    } catch (error) {
      toast({
        title: "Error",
        description: "Error al cargar los datos",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingLibro(null)
    setShowForm(true)
  }

  const handleEdit = (libro: Libro) => {
    setEditingLibro(libro)
    setShowForm(true)
  }

  const handleSave = async (libroData: Libro & { autores?: number[]; generos?: number[] }) => {
    if (!token) return

    try {
      if (editingLibro?.id) {
        await apiService.updateLibro(token, editingLibro.id, libroData)
        toast({
          title: "Éxito",
          description: "Libro actualizado correctamente",
        })
      } else {
        await apiService.createLibro(token, libroData)
        toast({
          title: "Éxito",
          description: "Libro creado correctamente",
        })
      }
      setShowForm(false)
      setEditingLibro(null)
      loadData()
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Error al guardar el libro",
        variant: "destructive",
      })
    }
  }

  const handleDelete = async (id: number) => {
    if (!token) return

    try {
      await apiService.deleteLibro(token, id)
      toast({
        title: "Éxito",
        description: "Libro eliminado correctamente",
      })
      loadData()
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Error al eliminar el libro",
        variant: "destructive",
      })
    }
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingLibro(null)
  }

  if (showFiltros) {
    return <LibrosPorFiltro autores={autores} generos={generos} onBack={() => setShowFiltros(false)} />
  }

  if (showForm) {
    return (
      <LibroForm libro={editingLibro} autores={autores} generos={generos} onSave={handleSave} onCancel={handleCancel} />
    )
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>Gestión de Libros</CardTitle>
          <div className="space-x-2">
            <Button onClick={() => setShowFiltros(true)} variant="outline">
              <Search className="mr-2 h-4 w-4" />
              Buscar por Filtros
            </Button>
            <Button onClick={handleCreate}>
              <Plus className="mr-2 h-4 w-4" />
              Nuevo Libro
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <LibroList libros={libros} isLoading={isLoading} onEdit={handleEdit} onDelete={handleDelete} />
      </CardContent>
    </Card>
  )
}
