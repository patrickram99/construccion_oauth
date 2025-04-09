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
            anio_publicacion INTEGER,
            genero_codigo VARCHAR(20) REFERENCES generos(codigo),
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
        SELECT l.*, g.nombre as genero_nombre
        FROM libros l
        LEFT JOIN generos g ON l.genero_codigo = g.codigo
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        libros = cursor.fetchall()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        result = []
        for libro in libros:
            libro_data = {
                'id': libro[0],
                'titulo': libro[1],
                'anio_publicacion': libro[2],
                'genero_codigo': libro[3],
                'isbn': libro[4],
                'descripcion': libro[5],
                'num_paginas': libro[6],
                'genero_nombre': libro[7]
            }
            
            # Obtener los autores del libro
            autores = self.get_autores_by_libro_id(libro[0])
            libro_data['autores'] = autores
            
            result.append(libro_data)
        return result

    def get_libro_by_id(self, libro_id):
        query = """
        SELECT l.*, g.nombre as genero_nombre
        FROM libros l
        LEFT JOIN generos g ON l.genero_codigo = g.codigo
        WHERE l.id = %s
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (libro_id,))
        libro = cursor.fetchone()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        if libro:
            libro_data = {
                'id': libro[0],
                'titulo': libro[1],
                'anio_publicacion': libro[2],
                'genero_codigo': libro[3],
                'isbn': libro[4],
                'descripcion': libro[5],
                'num_paginas': libro[6],
                'genero_nombre': libro[7]
            }
            
            # Obtener los autores del libro
            autores = self.get_autores_by_libro_id(libro_id)
            libro_data['autores'] = autores
            
            return libro_data
        return None

    def get_autores_by_libro_id(self, libro_id):
        query = """
        SELECT a.*
        FROM autores a
        JOIN libro_autor la ON a.id = la.autor_id
        WHERE la.libro_id = %s
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
                'biografia': autor[5]
            })
        return result

    def create_libro(self, libro_data):
        connection = self.connection_pool.get_connection()
        try:
            connection.autocommit = False
            cursor = connection.cursor()
            
            # Insertar el libro
            query = """
            INSERT INTO libros (titulo, anio_publicacion, genero_codigo, isbn, descripcion, num_paginas)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """
            cursor.execute(query, (
                libro_data['titulo'],
                libro_data.get('anio_publicacion'),
                libro_data.get('genero_codigo'),
                libro_data.get('isbn'),
                libro_data.get('descripcion'),
                libro_data.get('num_paginas')
            ))
            libro_id = cursor.fetchone()[0]
            
            # Si hay autores, asociarlos con el libro
            if 'autores' in libro_data and libro_data['autores']:
                for autor_id in libro_data['autores']:
                    query = """
                    INSERT INTO libro_autor (libro_id, autor_id)
                    VALUES (%s, %s)
                    """
                    cursor.execute(query, (libro_id, autor_id))
            
            connection.commit()
            return libro_id
            
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.autocommit = True
            cursor.close()
            self.connection_pool.release_connection(connection)

    def update_libro(self, libro_id, libro_data):
        connection = self.connection_pool.get_connection()
        try:
            connection.autocommit = False
            cursor = connection.cursor()
            
            # Actualizar información del libro
            query = """
            UPDATE libros 
            SET titulo = %s, anio_publicacion = %s, genero_codigo = %s, 
                isbn = %s, descripcion = %s, num_paginas = %s
            WHERE id = %s
            """
            cursor.execute(query, (
                libro_data['titulo'],
                libro_data.get('anio_publicacion'),
                libro_data.get('genero_codigo'),
                libro_data.get('isbn'),
                libro_data.get('descripcion'),
                libro_data.get('num_paginas'),
                libro_id
            ))
            
            # Si hay autores, actualizar las asociaciones
            if 'autores' in libro_data:
                # Eliminar las asociaciones existentes
                query = "DELETE FROM libro_autor WHERE libro_id = %s"
                cursor.execute(query, (libro_id,))
                
                # Crear nuevas asociaciones
                for autor_id in libro_data['autores']:
                    query = """
                    INSERT INTO libro_autor (libro_id, autor_id)
                    VALUES (%s, %s)
                    """
                    cursor.execute(query, (libro_id, autor_id))
            
            connection.commit()
            return True
            
        except Exception as e:
            connection.rollback()
            return False
        finally:
            connection.autocommit = True
            cursor.close()
            self.connection_pool.release_connection(connection)

    def delete_libro(self, libro_id):
        connection = self.connection_pool.get_connection()
        try:
            connection.autocommit = False
            cursor = connection.cursor()
            
            # Eliminar las asociaciones con autores
            query = "DELETE FROM libro_autor WHERE libro_id = %s"
            cursor.execute(query, (libro_id,))
            
            # Eliminar el libro
            query = "DELETE FROM libros WHERE id = %s"
            cursor.execute(query, (libro_id,))
            rows_affected = cursor.rowcount
            
            connection.commit()
            return rows_affected > 0
            
        except Exception as e:
            connection.rollback()
            return False
        finally:
            connection.autocommit = True
            cursor.close()
            self.connection_pool.release_connection(connection)