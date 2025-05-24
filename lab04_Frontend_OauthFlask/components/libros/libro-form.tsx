"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import type { Libro, Autor, Genero } from "@/services/api"
import { ArrowLeft } from "lucide-react"

interface LibroFormProps {
  libro: Libro | null
  autores: Autor[]
  generos: Genero[]
  onSave: (libro: Libro & { autores?: number[]; generos?: number[] }) => void
  onCancel: () => void
}

export function LibroForm({ libro, autores, generos, onSave, onCancel }: LibroFormProps) {
  const [formData, setFormData] = useState<Libro>({
    titulo: "",
    isbn: "",
    fecha_publicacion: "",
    descripcion: "",
  })
  const [selectedAutores, setSelectedAutores] = useState<number[]>([])
  const [selectedGeneros, setSelectedGeneros] = useState<number[]>([])

  useEffect(() => {
    if (libro) {
      setFormData({
        titulo: libro.titulo || "",
        isbn: libro.isbn || "",
        fecha_publicacion: libro.fecha_publicacion || "",
        descripcion: libro.descripcion || "",
      })
      setSelectedAutores(libro.autores?.map((a) => a.id!).filter(Boolean) || [])
      setSelectedGeneros(libro.generos?.map((g) => g.id!).filter(Boolean) || [])
    }
  }, [libro])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave({
      ...formData,
      autores: selectedAutores,
      generos: selectedGeneros,
    })
  }

  const handleChange = (field: keyof Libro, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const handleAutorChange = (autorId: number, checked: boolean) => {
    setSelectedAutores((prev) => (checked ? [...prev, autorId] : prev.filter((id) => id !== autorId)))
  }

  const handleGeneroChange = (generoId: number, checked: boolean) => {
    setSelectedGeneros((prev) => (checked ? [...prev, generoId] : prev.filter((id) => id !== generoId)))
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={onCancel}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <CardTitle>{libro ? "Editar Libro" : "Nuevo Libro"}</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="titulo">Título *</Label>
              <Input
                id="titulo"
                value={formData.titulo}
                onChange={(e) => handleChange("titulo", e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="isbn">ISBN</Label>
              <Input id="isbn" value={formData.isbn} onChange={(e) => handleChange("isbn", e.target.value)} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="fecha_publicacion">Fecha de Publicación</Label>
              <Input
                id="fecha_publicacion"
                type="date"
                value={formData.fecha_publicacion}
                onChange={(e) => handleChange("fecha_publicacion", e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="descripcion">Descripción</Label>
            <Textarea
              id="descripcion"
              value={formData.descripcion}
              onChange={(e) => handleChange("descripcion", e.target.value)}
              rows={3}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <Label>Autores</Label>
              <div className="space-y-2 max-h-40 overflow-y-auto border rounded p-3">
                {autores.map((autor) => (
                  <div key={autor.id} className="flex items-center space-x-2">
                    <Checkbox
                      id={`autor-${autor.id}`}
                      checked={selectedAutores.includes(autor.id!)}
                      onCheckedChange={(checked) => handleAutorChange(autor.id!, checked as boolean)}
                    />
                    <Label htmlFor={`autor-${autor.id}`} className="text-sm">
                      {autor.nombre} {autor.apellido}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-3">
              <Label>Géneros</Label>
              <div className="space-y-2 max-h-40 overflow-y-auto border rounded p-3">
                {generos.map((genero) => (
                  <div key={genero.id} className="flex items-center space-x-2">
                    <Checkbox
                      id={`genero-${genero.id}`}
                      checked={selectedGeneros.includes(genero.id!)}
                      onCheckedChange={(checked) => handleGeneroChange(genero.id!, checked as boolean)}
                    />
                    <Label htmlFor={`genero-${genero.id}`} className="text-sm">
                      {genero.nombre}
                    </Label>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="flex gap-2">
            <Button type="submit">{libro ? "Actualizar" : "Crear"} Libro</Button>
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancelar
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
