from db.connection_pool import PostgreSQLConnectionPool
import psycopg2.extras

class Autor:
    def __init__(self, id=None, nombre=None, apellido=None, fecha_nacimiento=None, nacionalidad=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.nacionalidad = nacionalidad
    
    @staticmethod
    def get_all():
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM autor ORDER BY apellido, nombre")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching autores: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def get_by_id(autor_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM autor WHERE id = %s", (autor_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching autor: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    def save(self):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            if self.id:
                cursor.execute("""
                UPDATE autor SET nombre = %s, apellido = %s, fecha_nacimiento = %s, nacionalidad = %s, 
                updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *
                """, (self.nombre, self.apellido, self.fecha_nacimiento, self.nacionalidad, self.id))
            else:
                cursor.execute("""
                INSERT INTO autor (nombre, apellido, fecha_nacimiento, nacionalidad) 
                VALUES (%s, %s, %s, %s) RETURNING *
                """, (self.nombre, self.apellido, self.fecha_nacimiento, self.nacionalidad))
            
            conn.commit()
            return cursor.fetchone()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error saving autor: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def delete(autor_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM autor WHERE id = %s RETURNING id", (autor_id,))
            result = cursor.fetchone()
            conn.commit()
            return result is not None
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error deleting autor: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)