from backend.models.postgresql_connection_pool import PostgreSQLConnectionPool
import json

class LibroModel:
    def __init__(self):
        self.connection_pool = PostgreSQLConnectionPool.get_instance()
        self.__create_table()

    def __create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS libros (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            autor_id INTEGER REFERENCES autores(id),
            anio_publicacion INTEGER,
            genero VARCHAR(100),
            isbn VARCHAR(20) UNIQUE,
            descripcion TEXT,
            num_paginas INTEGER
        )
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)

    def get_all_libros(self):
        query = """
        SELECT l.*, a.nombre, a.apellido
        FROM libros l
        LEFT JOIN autores a ON l.autor_id = a.id
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        libros = cursor.fetchall()
        cursor.close()
        self.connection_pool.release
        # postgresql_libro_model.py (continuación)
        libros = cursor.fetchall()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        result = []
        for libro in libros:
            result.append({
                'id': libro[0],
                'titulo': libro[1],
                'autor_id': libro[2],
                'anio_publicacion': libro[3],
                'genero': libro[4],
                'isbn': libro[5],
                'descripcion': libro[6],
                'num_paginas': libro[7],
                'autor_nombre': libro[8],
                'autor_apellido': libro[9]
            })
        return result

    def get_libro_by_id(self, libro_id):
        query = """
        SELECT l.*, a.nombre, a.apellido
        FROM libros l
        LEFT JOIN autores a ON l.autor_id = a.id
        WHERE l.id = %s
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (libro_id,))
        libro = cursor.fetchone()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        if libro:
            return {
                'id': libro[0],
                'titulo': libro[1],
                'autor_id': libro[2],
                'anio_publicacion': libro[3],
                'genero': libro[4],
                'isbn': libro[5],
                'descripcion': libro[6],
                'num_paginas': libro[7],
                'autor_nombre': libro[8],
                'autor_apellido': libro[9]
            }
        return None

    def create_libro(self, libro_data):
        query = """
        INSERT INTO libros (titulo, autor_id, anio_publicacion, genero, isbn, descripcion, num_paginas)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (
            libro_data['titulo'],
            libro_data.get('autor_id'),
            libro_data.get('anio_publicacion'),
            libro_data.get('genero'),
            libro_data.get('isbn'),
            libro_data.get('descripcion'),
            libro_data.get('num_paginas')
        ))
        libro_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return libro_id

    def update_libro(self, libro_id, libro_data):
        query = """
        UPDATE libros 
        SET titulo = %s, autor_id = %s, anio_publicacion = %s, genero = %s, 
            isbn = %s, descripcion = %s, num_paginas = %s
        WHERE id = %s
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (
            libro_data['titulo'],
            libro_data.get('autor_id'),
            libro_data.get('anio_publicacion'),
            libro_data.get('genero'),
            libro_data.get('isbn'),
            libro_data.get('descripcion'),
            libro_data.get('num_paginas'),
            libro_id
        ))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return rows_affected > 0

    def delete_libro(self, libro_id):
        query = "DELETE FROM libros WHERE id = %s"
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (libro_id,))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return rows_affected > 0