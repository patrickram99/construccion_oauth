"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Autor } from "@/services/api"
import { ArrowLeft } from "lucide-react"

interface AutorFormProps {
  autor: Autor | null
  onSave: (autor: Autor) => void
  onCancel: () => void
}

export function AutorForm({ autor, onSave, onCancel }: AutorFormProps) {
  const [formData, setFormData] = useState<Autor>({
    nombre: "",
    apellido: "",
    fecha_nacimiento: "",
    nacionalidad: "",
  })

  useEffect(() => {
    if (autor) {
      setFormData({
        nombre: autor.nombre || "",
        apellido: autor.apellido || "",
        fecha_nacimiento: autor.fecha_nacimiento || "",
        nacionalidad: autor.nacionalidad || "",
      })
    }
  }, [autor])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave(formData)
  }

  const handleChange = (field: keyof Autor, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={onCancel}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <CardTitle>{autor ? "Editar Autor" : "Nuevo Autor"}</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="nombre">Nombre *</Label>
              <Input
                id="nombre"
                value={formData.nombre}
                onChange={(e) => handleChange("nombre", e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="apellido">Apellido *</Label>
              <Input
                id="apellido"
                value={formData.apellido}
                onChange={(e) => handleChange("apellido", e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="fecha_nacimiento">Fecha de Nacimiento</Label>
              <Input
                id="fecha_nacimiento"
                type="date"
                value={formData.fecha_nacimiento}
                onChange={(e) => handleChange("fecha_nacimiento", e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="nacionalidad">Nacionalidad</Label>
              <Input
                id="nacionalidad"
                value={formData.nacionalidad}
                onChange={(e) => handleChange("nacionalidad", e.target.value)}
              />
            </div>
          </div>
          <div className="flex gap-2">
            <Button type="submit">{autor ? "Actualizar" : "Crear"} Autor</Button>
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancelar
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
