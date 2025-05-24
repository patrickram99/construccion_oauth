"use client"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useAuth } from "@/contexts/auth-context"
import { AutoresManager } from "@/components/autores/autores-manager"
import { GenerosManager } from "@/components/generos/generos-manager"
import { LibrosManager } from "@/components/libros/libros-manager"
import { LogOut, Book, Users, Tag } from "lucide-react"

export function Dashboard() {
  const { logout } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-3xl font-bold text-gray-900">Sistema de Gestión de Biblioteca</h1>
            <Button onClick={logout} variant="outline">
              <LogOut className="mr-2 h-4 w-4" />
              Cerrar Sesión
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <Tabs defaultValue="libros" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="libros" className="flex items-center gap-2">
              <Book className="h-4 w-4" />
              Libros
            </TabsTrigger>
            <TabsTrigger value="autores" className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              Autores
            </TabsTrigger>
            <TabsTrigger value="generos" className="flex items-center gap-2">
              <Tag className="h-4 w-4" />
              Géneros
            </TabsTrigger>
          </TabsList>

          <TabsContent value="libros">
            <LibrosManager />
          </TabsContent>

          <TabsContent value="autores">
            <AutoresManager />
          </TabsContent>

          <TabsContent value="generos">
            <GenerosManager />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
