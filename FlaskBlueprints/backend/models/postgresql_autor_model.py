from backend.models.postgresql_connection_pool import PostgreSQLConnectionPool
import json

class AutorModel:
    def __init__(self):
        self.connection_pool = PostgreSQLConnectionPool.get_instance()
        self.__create_table()

    def __create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS autores (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            fecha_nacimiento DATE,
            nacionalidad VARCHAR(100),
            biografia TEXT
        )
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)

    def get_all_autores(self):
        query = "SELECT * FROM autores"
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
                'biografia': autor[5]
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
                'biografia': autor[5]
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
        query = """
        UPDATE autores 
        SET nombre = %s, apellido = %s, fecha_nacimiento = %s, nacionalidad = %s, biografia = %s
        WHERE id = %s
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (
            autor_data['nombre'],
            autor_data['apellido'],
            autor_data.get('fecha_nacimiento'),
            autor_data.get('nacionalidad'),
            autor_data.get('biografia'),
            autor_id
        ))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return rows_affected > 0

    def delete_autor(self, autor_id):
        query = "DELETE FROM autores WHERE id = %s"
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (autor_id,))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return rows_affected > 0