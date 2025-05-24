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
import type { Autor } from "@/services/api"
import { Edit, Trash2 } from "lucide-react"

interface AutorListProps {
  autores: Autor[]
  isLoading: boolean
  onEdit: (autor: Autor) => void
  onDelete: (id: number) => void
}

export function AutorList({ autores, isLoading, onEdit, onDelete }: AutorListProps) {
  if (isLoading) {
    return <div className="text-center py-4">Cargando autores...</div>
  }

  if (autores.length === 0) {
    return <div className="text-center py-4 text-gray-500">No hay autores registrados</div>
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Nombre</TableHead>
          <TableHead>Apellido</TableHead>
          <TableHead>Fecha de Nacimiento</TableHead>
          <TableHead>Nacionalidad</TableHead>
          <TableHead className="text-right">Acciones</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {autores.map((autor) => (
          <TableRow key={autor.id}>
            <TableCell>{autor.nombre}</TableCell>
            <TableCell>{autor.apellido}</TableCell>
            <TableCell>
              {autor.fecha_nacimiento ? new Date(autor.fecha_nacimiento).toLocaleDateString() : "-"}
            </TableCell>
            <TableCell>{autor.nacionalidad || "-"}</TableCell>
            <TableCell className="text-right">
              <div className="flex gap-2 justify-end">
                <Button variant="outline" size="icon" onClick={() => onEdit(autor)}>
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
                        Esta acción no se puede deshacer. Se eliminará permanentemente el autor{" "}
                        <strong>
                          {autor.nombre} {autor.apellido}
                        </strong>
                        .
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancelar</AlertDialogCancel>
                      <AlertDialogAction onClick={() => autor.id && onDelete(autor.id)}>Eliminar</AlertDialogAction>
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
