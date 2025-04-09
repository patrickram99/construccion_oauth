from backend.models.postgresql_connection_pool import PostgreSQLConnectionPool

class LibroAutorModel:
    def __init__(self):
        self.connection_pool = PostgreSQLConnectionPool.get_instance()
        self.__create_table()

    def __create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS libro_autor (
            libro_id INTEGER REFERENCES libros(id) ON DELETE CASCADE,
            autor_id INTEGER REFERENCES autores(id) ON DELETE CASCADE,
            orden INTEGER DEFAULT 1,
            rol VARCHAR(50) DEFAULT 'Autor principal',
            PRIMARY KEY (libro_id, autor_id)
        )
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)

    def get_libros_by_autor_id(self, autor_id):
        query = """
        SELECT l.*, g.nombre as genero_nombre
        FROM libros l
        JOIN libro_autor la ON l.id = la.libro_id
        LEFT JOIN generos g ON l.genero_codigo = g.codigo
        WHERE la.autor_id = %s
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (autor_id,))
        libros = cursor.fetchall()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        result = []
        for libro in libros:
            result.append({
                'id': libro[0],
                'titulo': libro[1],
                'anio_publicacion': libro[2],
                'genero_codigo': libro[3],
                'isbn': libro[4],
                'descripcion': libro[5],
                'num_paginas': libro[6],
                'genero_nombre': libro[7]
            })
        return result

    def asignar_autor_a_libro(self, libro_id, autor_id, orden=1, rol='Autor principal'):
        query = """
        INSERT INTO libro_autor (libro_id, autor_id, orden, rol)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (libro_id, autor_id) DO UPDATE 
        SET orden = %s, rol = %s
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (libro_id, autor_id, orden, rol, orden, rol))
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return True

    def eliminar_autor_de_libro(self, libro_id, autor_id):
        query = """
        DELETE FROM libro_autor 
        WHERE libro_id = %s AND autor_id = %s
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (libro_id, autor_id))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return rows_affected > 0

    def get_autores_by_libro_id(self, libro_id):
        query = """
        SELECT a.*, la.orden, la.rol
        FROM autores a
        JOIN libro_autor la ON a.id = la.autor_id
        WHERE la.libro_id = %s
        ORDER BY la.orden
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (libro_id,))
        autores = cursor.fetchall()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        result = []
        for autor in autores:
            result.append({
                'id': autor[0],
                'nombre': autor[1],
                'apellido': autor[2],
                'fecha_nacimiento': autor[3].strftime('%Y-%m-%d') if autor[3] else None,
                'nacionalidad': autor[4],
                'biografia': autor[5],
                'orden': autor[6],
                'rol': autor[7]
            })
        return result