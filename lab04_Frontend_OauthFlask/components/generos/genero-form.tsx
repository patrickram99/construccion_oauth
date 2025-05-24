"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Genero } from "@/services/api"
import { ArrowLeft } from "lucide-react"

interface GeneroFormProps {
  genero: Genero | null
  onSave: (genero: Genero) => void
  onCancel: () => void
}

export function GeneroForm({ genero, onSave, onCancel }: GeneroFormProps) {
  const [formData, setFormData] = useState<Genero>({
    nombre: "",
    descripcion: "",
  })

  useEffect(() => {
    if (genero) {
      setFormData({
        nombre: genero.nombre || "",
        descripcion: genero.descripcion || "",
      })
    }
  }, [genero])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave(formData)
  }

  const handleChange = (field: keyof Genero, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={onCancel}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <CardTitle>{genero ? "Editar Género" : "Nuevo Género"}</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
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
            <Label htmlFor="descripcion">Descripción</Label>
            <Textarea
              id="descripcion"
              value={formData.descripcion}
              onChange={(e) => handleChange("descripcion", e.target.value)}
              rows={3}
            />
          </div>
          <div className="flex gap-2">
            <Button type="submit">{genero ? "Actualizar" : "Crear"} Género</Button>
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancelar
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
