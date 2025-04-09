from backend.models.postgresql_connection_pool import PostgreSQLConnectionPool
import json

class GeneroModel:
    def __init__(self):
        self.connection_pool = PostgreSQLConnectionPool.get_instance()
        self.__create_table()

    def __create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS generos (
            id SERIAL PRIMARY KEY,
            codigo VARCHAR(20) UNIQUE NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT
        )
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)

    def get_all_generos(self):
        query = "SELECT * FROM generos"
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        generos = cursor.fetchall()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        result = []
        for genero in generos:
            result.append({
                'id': genero[0],
                'codigo': genero[1],
                'nombre': genero[2],
                'descripcion': genero[3]
            })
        return result

    def get_genero_by_id(self, genero_id):
        query = "SELECT * FROM generos WHERE id = %s"
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (genero_id,))
        genero = cursor.fetchone()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        if genero:
            return {
                'id': genero[0],
                'codigo': genero[1],
                'nombre': genero[2],
                'descripcion': genero[3]
            }
        return None

    def get_genero_by_codigo(self, codigo):
        query = "SELECT * FROM generos WHERE codigo = %s"
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (codigo,))
        genero = cursor.fetchone()
        cursor.close()
        self.connection_pool.release_connection(connection)
        
        if genero:
            return {
                'id': genero[0],
                'codigo': genero[1],
                'nombre': genero[2],
                'descripcion': genero[3]
            }
        return None

    def create_genero(self, genero_data):
        query = """
        INSERT INTO generos (codigo, nombre, descripcion)
        VALUES (%s, %s, %s) RETURNING id
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (
            genero_data['codigo'],
            genero_data['nombre'],
            genero_data.get('descripcion')
        ))
        genero_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return genero_id

    def update_genero(self, genero_id, genero_data):
        query = """
        UPDATE generos 
        SET codigo = %s, nombre = %s, descripcion = %s
        WHERE id = %s
        """
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (
            genero_data['codigo'],
            genero_data['nombre'],
            genero_data.get('descripcion'),
            genero_id
        ))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return rows_affected > 0

    def delete_genero(self, genero_id):
        query = "DELETE FROM generos WHERE id = %s"
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (genero_id,))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        self.connection_pool.release_connection(connection)
        return rows_affected > 0