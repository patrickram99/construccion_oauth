"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { useAuth } from "@/contexts/auth-context"
import { useToast } from "@/hooks/use-toast"
import { apiService, type Libro, type Autor, type Genero } from "@/services/api"
import { ArrowLeft, Users, Tag } from "lucide-react"

interface LibrosPorFiltroProps {
  autores: Autor[]
  generos: Genero[]
  onBack: () => void
}

export function LibrosPorFiltro({ autores, generos, onBack }: LibrosPorFiltroProps) {
  const [libros, setLibros] = useState<Libro[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [selectedAutor, setSelectedAutor] = useState<string>("")
  const [selectedGenero, setSelectedGenero] = useState<string>("")
  const [filtroActivo, setFiltroActivo] = useState<"autor" | "genero" | null>(null)
  const { token } = useAuth()
  const { toast } = useToast()

  const buscarLibrosPorAutor = async (autorId: string) => {
    if (!token || !autorId) return

    try {
      setIsLoading(true)
      setFiltroActivo("autor")
      const data = await apiService.getLibrosPorAutor(token, Number.parseInt(autorId))
      setLibros(data)
      setSelectedGenero("")
    } catch (error) {
      toast({
        title: "Error",
        description: "Error al buscar libros por autor",
        variant: "destructive",
      })
      setLibros([])
    } finally {
      setIsLoading(false)
    }
  }

  const buscarLibrosPorGenero = async (generoId: string) => {
    if (!token || !generoId) return

    try {
      setIsLoading(true)
      setFiltroActivo("genero")
      const data = await apiService.getLibrosPorGenero(token, Number.parseInt(generoId))
      setLibros(data)
      setSelectedAutor("")
    } catch (error) {
      toast({
        title: "Error",
        description: "Error al buscar libros por género",
        variant: "destructive",
      })
      setLibros([])
    } finally {
      setIsLoading(false)
    }
  }

  const limpiarFiltros = () => {
    setLibros([])
    setSelectedAutor("")
    setSelectedGenero("")
    setFiltroActivo(null)
  }

  const autorSeleccionado = autores.find((a) => a.id?.toString() === selectedAutor)
  const generoSeleccionado = generos.find((g) => g.id?.toString() === selectedGenero)

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={onBack}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <CardTitle>Buscar Libros por Filtros</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Filtros */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2">
              <Users className="h-4 w-4" />
              Buscar por Autor
            </label>
            <div className="flex gap-2">
              <Select value={selectedAutor} onValueChange={setSelectedAutor}>
                <SelectTrigger>
                  <SelectValue placeholder="Seleccionar autor" />
                </SelectTrigger>
                <SelectContent>
                  {autores.map((autor) => (
                    <SelectItem key={autor.id} value={autor.id?.toString() || ""}>
                      {autor.nombre} {autor.apellido}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button onClick={() => buscarLibrosPorAutor(selectedAutor)} disabled={!selectedAutor || isLoading}>
                Buscar
              </Button>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2">
              <Tag className="h-4 w-4" />
              Buscar por Género
            </label>
            <div className="flex gap-2">
              <Select value={selectedGenero} onValueChange={setSelectedGenero}>
                <SelectTrigger>
                  <SelectValue placeholder="Seleccionar género" />
                </SelectTrigger>
                <SelectContent>
                  {generos.map((genero) => (
                    <SelectItem key={genero.id} value={genero.id?.toString() || ""}>
                      {genero.nombre}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button onClick={() => buscarLibrosPorGenero(selectedGenero)} disabled={!selectedGenero || isLoading}>
                Buscar
              </Button>
            </div>
          </div>
        </div>

        {/* Botón limpiar */}
        {(selectedAutor || selectedGenero || libros.length > 0) && (
          <div className="flex justify-center">
            <Button variant="outline" onClick={limpiarFiltros}>
              Limpiar Filtros
            </Button>
          </div>
        )}

        {/* Filtro activo */}
        {filtroActivo && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Mostrando libros de:</span>
            {filtroActivo === "autor" && autorSeleccionado && (
              <Badge variant="secondary">
                <Users className="h-3 w-3 mr-1" />
                {autorSeleccionado.nombre} {autorSeleccionado.apellido}
              </Badge>
            )}
            {filtroActivo === "genero" && generoSeleccionado && (
              <Badge variant="outline">
                <Tag className="h-3 w-3 mr-1" />
                {generoSeleccionado.nombre}
              </Badge>
            )}
          </div>
        )}

        {/* Resultados */}
        {isLoading ? (
          <div className="text-center py-8">
            <div className="text-gray-500">Buscando libros...</div>
          </div>
        ) : libros.length > 0 ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">
                Resultados ({libros.length} libro{libros.length !== 1 ? "s" : ""})
              </h3>
            </div>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Título</TableHead>
                  <TableHead>ISBN</TableHead>
                  <TableHead>Fecha de Publicación</TableHead>
                  <TableHead>Descripción</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {libros.map((libro) => (
                  <TableRow key={libro.id}>
                    <TableCell className="font-medium">{libro.titulo}</TableCell>
                    <TableCell>{libro.isbn || "-"}</TableCell>
                    <TableCell>
                      {libro.fecha_publicacion ? new Date(libro.fecha_publicacion).toLocaleDateString() : "-"}
                    </TableCell>
                    <TableCell className="max-w-xs">
                      <div className="truncate" title={libro.descripcion}>
                        {libro.descripcion || "-"}
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        ) : filtroActivo && !isLoading ? (
          <div className="text-center py-8">
            <div className="text-gray-500">No se encontraron libros para el filtro seleccionado</div>
          </div>
        ) : null}
      </CardContent>
    </Card>
  )
}
