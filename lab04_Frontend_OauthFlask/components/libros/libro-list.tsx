"use client"

import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import type { Libro } from "@/services/api"
import { Edit, Trash2 } from "lucide-react"

interface LibroListProps {
  libros: Libro[]
  isLoading: boolean
  onEdit: (libro: Libro) => void
  onDelete: (id: number) => void
}

export function LibroList({ libros, isLoading, onEdit, onDelete }: LibroListProps) {
  if (isLoading) {
    return <div className="text-center py-4">Cargando libros...</div>
  }

  if (libros.length === 0) {
    return <div className="text-center py-4 text-gray-500">No hay libros registrados</div>
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Título</TableHead>
          <TableHead>ISBN</TableHead>
          <TableHead>Fecha de Publicación</TableHead>
          <TableHead className="text-right">Acciones</TableHead>
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
            <TableCell className="text-right">
              <div className="flex gap-2 justify-end">
                <Button variant="outline" size="icon" onClick={() => onEdit(libro)}>
                  <Edit className="h-4 w-4" />
                </Button>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button variant="outline" size="icon">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>¿Estás seguro?</AlertDialogTitle>
                      <AlertDialogDescription>
                        Esta acción no se puede deshacer. Se eliminará permanentemente el libro{" "}
                        <strong>{libro.titulo}</strong>.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancelar</AlertDialogCancel>
                      <AlertDialogAction onClick={() => libro.id && onDelete(libro.id)}>Eliminar</AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
