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
import type { Genero } from "@/services/api"
import { Edit, Trash2 } from "lucide-react"

interface GeneroListProps {
  generos: Genero[]
  isLoading: boolean
  onEdit: (genero: Genero) => void
  onDelete: (id: number) => void
}

export function GeneroList({ generos, isLoading, onEdit, onDelete }: GeneroListProps) {
  if (isLoading) {
    return <div className="text-center py-4">Cargando géneros...</div>
  }

  if (generos.length === 0) {
    return <div className="text-center py-4 text-gray-500">No hay géneros registrados</div>
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Nombre</TableHead>
          <TableHead>Descripción</TableHead>
          <TableHead className="text-right">Acciones</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {generos.map((genero) => (
          <TableRow key={genero.id}>
            <TableCell className="font-medium">{genero.nombre}</TableCell>
            <TableCell>{genero.descripcion || "-"}</TableCell>
            <TableCell className="text-right">
              <div className="flex gap-2 justify-end">
                <Button variant="outline" size="icon" onClick={() => onEdit(genero)}>
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
                        Esta acción no se puede deshacer. Se eliminará permanentemente el género{" "}
                        <strong>{genero.nombre}</strong>.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancelar</AlertDialogCancel>
                      <AlertDialogAction onClick={() => genero.id && onDelete(genero.id)}>Eliminar</AlertDialogAction>
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
