from backend.models.postgresql_connection_pool import PostgreSQLConnectionPool
import json

class AutorModel:
    def __init__(self):
        self.connection_pool = PostgreSQLConnectionPool.get_instance()
        self.__create_table()

    def __create_table(self):
        # Create tables in correct order based on dependencies
        generos_query = """
        CREATE TABLE IF NOT EXISTS generos (
            id SERIAL PRIMARY KEY,
            codigo VARCHAR(20) UNIQUE NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT
        )
        """
        
        libros_query = """
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
        
        autores_query = """
        CREATE TABLE IF NOT EXISTS autores (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            fecha_nacimiento DATE,
            nacionalidad VARCHAR(100),
            biografia TEXT,
            eliminado BOOLEAN DEFAULT FALSE
        )
        """
        
        libro_autor_query = """
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
        
        try:
            # Execute the creation of tables in correct dependency order
            cursor.execute(generos_query)      # 1. Create generos first (no dependencies)
            cursor.execute(libros_query)       # 2. Create libros (depends on generos)
            cursor.execute(autores_query)      # 3. Create autores (no dependencies)
            cursor.execute(libro_autor_query)  # 4. Create libro_autor (depends on libros and autores)
            connection.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")
            connection.rollback()
            raise e
        finally:
            cursor.close()
            self.connection_pool.release_connection(connection)



    def get_all_autores(self, incluir_eliminados=False):
        if incluir_eliminados:
            query = "SELECT * FROM autores"
        else:
            query = "SELECT * FROM autores WHERE eliminado = FALSE"
            
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
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
                'eliminado': autor[6]
            })
        return result

    def get_autor_by_id(self, autor_id):
        query = "SELECT * FROM autores WHERE id = %s"
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (autor_id,))
        autor = cursor.fetchone()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        if autor:
            return {
                'id': autor[0],
                'nombre': autor[1],
                'apellido': autor[2],
                'fecha_nacimiento': autor[3].strftime('%Y-%m-%d') if autor[3] else None,
                'nacionalidad': autor[4],
                'biografia': autor[5],
                'eliminado': autor[6]
            }
        return None

    def create_autor(self, autor_data):
        query = """
        INSERT INTO autores (nombre, apellido, fecha_nacimiento, nacionalidad, biografia)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (
            autor_data['nombre'],
            autor_data['apellido'],
            autor_data.get('fecha_nacimiento'),
            autor_data.get('nacionalidad'),
            autor_data.get('biografia')
        ))
        autor_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return autor_id

    def update_autor(self, autor_id, autor_data):
        # Primero obtenemos los datos actuales para actualizar solo lo que cambia
        autor_actual = self.get_autor_by_id(autor_id)
        if not autor_actual:
            return False
            
        # Combinamos los datos actuales con los nuevos
        nombre = autor_data.get('nombre', autor_actual['nombre'])
        apellido = autor_data.get('apellido', autor_actual['apellido'])
        fecha_nacimiento = autor_data.get('fecha_nacimiento', autor_actual['fecha_nacimiento'])
        nacionalidad = autor_data.get('nacionalidad', autor_actual['nacionalidad'])
        biografia = autor_data.get('biografia', autor_actual['biografia'])
        
        query = """
        UPDATE autores 
        SET nombre = %s, apellido = %s, fecha_nacimiento = %s, nacionalidad = %s, biografia = %s
        WHERE id = %s AND eliminado = FALSE
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (
            nombre,
            apellido,
            fecha_nacimiento,
            nacionalidad,
            biografia,
            autor_id
        ))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return rows_affected > 0

def delete_autor(self, autor_id, borrado_fisico=False):
    if borrado_fisico:
        query = "DELETE FROM autores WHERE id = %s"
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (autor_id,))
    else:
        # Borrado lógico - solo marcamos como eliminado
        query = "UPDATE autores SET eliminado = TRUE WHERE id = %s AND eliminado = FALSE"
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (autor_id,))
    
    rows_affected = cursor.rowcount
    connection.commit()
    cursor.close()
    self.connection_pool.release_connection(connection)
    return rows_affected > 0

def restaurar_autor(self, autor_id):
    query = "UPDATE autores SET eliminado = FALSE WHERE id = %s AND eliminado = TRUE"
    connection = self.connection_pool.get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (autor_id,))
    rows_affected = cursor.rowcount
    connection.commit()
    cursor.close()
    self.connection_pool.release_connection(connection)
    return rows_affected > 0