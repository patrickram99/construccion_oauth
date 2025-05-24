const API_BASE_URL = "http://localhost:5000/api"

export interface Autor {
  id?: number
  nombre: string
  apellido: string
  fecha_nacimiento?: string
  nacionalidad?: string
}

export interface Genero {
  id?: number
  nombre: string
  descripcion?: string
}

export interface Libro {
  id?: number
  titulo: string
  isbn?: string
  fecha_publicacion?: string
  descripcion?: string
  autores?: Autor[]
  generos?: Genero[]
}

class ApiService {
  private getHeaders(token: string) {
    return {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    }
  }

  private async handleResponse(response: Response) {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`)
    }
    return response.json()
  }

  // Autores
  async getAutores(token: string): Promise<Autor[]> {
    const response = await fetch(`${API_BASE_URL}/autores/`, {
      headers: this.getHeaders(token),
    })
    return this.handleResponse(response)
  }

  async getAutor(token: string, id: number): Promise<Autor> {
    const response = await fetch(`${API_BASE_URL}/autores/${id}`, {
      headers: this.getHeaders(token),
    })
    return this.handleResponse(response)
  }

  async createAutor(token: string, autor: Autor): Promise<Autor> {
    const response = await fetch(`${API_BASE_URL}/autores/`, {
      method: "POST",
      headers: this.getHeaders(token),
      body: JSON.stringify(autor),
    })
    return this.handleResponse(response)
  }

  async updateAutor(token: string, id: number, autor: Autor): Promise<Autor> {
    const response = await fetch(`${API_BASE_URL}/autores/${id}`, {
      method: "PUT",
      headers: this.getHeaders(token),
      body: JSON.stringify(autor),
    })
    return this.handleResponse(response)
  }

  async deleteAutor(token: string, id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/autores/${id}`, {
      method: "DELETE",
      headers: this.getHeaders(token),
    })
    await this.handleResponse(response)
  }

  // Géneros
  async getGeneros(token: string): Promise<Genero[]> {
    const response = await fetch(`${API_BASE_URL}/generos/`, {
      headers: this.getHeaders(token),
    })
    return this.handleResponse(response)
  }

  async getGenero(token: string, id: number): Promise<Genero> {
    const response = await fetch(`${API_BASE_URL}/generos/${id}`, {
      headers: this.getHeaders(token),
    })
    return this.handleResponse(response)
  }

  async createGenero(token: string, genero: Genero): Promise<Genero> {
    const response = await fetch(`${API_BASE_URL}/generos/`, {
      method: "POST",
      headers: this.getHeaders(token),
      body: JSON.stringify(genero),
    })
    return this.handleResponse(response)
  }

  async updateGenero(token: string, id: number, genero: Genero): Promise<Genero> {
    const response = await fetch(`${API_BASE_URL}/generos/${id}`, {
      method: "PUT",
      headers: this.getHeaders(token),
      body: JSON.stringify(genero),
    })
    return this.handleResponse(response)
  }

  async deleteGenero(token: string, id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/generos/${id}`, {
      method: "DELETE",
      headers: this.getHeaders(token),
    })
    await this.handleResponse(response)
  }

  // Libros
  async getLibros(token: string): Promise<Libro[]> {
    const response = await fetch(`${API_BASE_URL}/libros/`, {
      headers: this.getHeaders(token),
    })
    return this.handleResponse(response)
  }

  async getLibro(token: string, id: number): Promise<Libro> {
    const response = await fetch(`${API_BASE_URL}/libros/${id}`, {
      headers: this.getHeaders(token),
    })
    return this.handleResponse(response)
  }

  async createLibro(token: string, libro: Libro & { autores?: number[]; generos?: number[] }): Promise<Libro> {
    const response = await fetch(`${API_BASE_URL}/libros/`, {
      method: "POST",
      headers: this.getHeaders(token),
      body: JSON.stringify(libro),
    })
    return this.handleResponse(response)
  }

  async updateLibro(
    token: string,
    id: number,
    libro: Libro & { autores?: number[]; generos?: number[] },
  ): Promise<Libro> {
    const response = await fetch(`${API_BASE_URL}/libros/${id}`, {
      method: "PUT",
      headers: this.getHeaders(token),
      body: JSON.stringify(libro),
    })
    return this.handleResponse(response)
  }

  async deleteLibro(token: string, id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/libros/${id}`, {
      method: "DELETE",
      headers: this.getHeaders(token),
    })
    await this.handleResponse(response)
  }

  async getLibrosPorGenero(token: string, generoId: number): Promise<Libro[]> {
    const response = await fetch(`${API_BASE_URL}/libros/por-genero/${generoId}`, {
      headers: this.getHeaders(token),
    })
    return this.handleResponse(response)
  }

  async getLibrosPorAutor(token: string, autorId: number): Promise<Libro[]> {
    const response = await fetch(`${API_BASE_URL}/libros/por-autor/${autorId}`, {
      headers: this.getHeaders(token),
    })
    return this.handleResponse(response)
  }
}

export const apiService = new ApiService()
