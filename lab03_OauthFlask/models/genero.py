from db.connection_pool import PostgreSQLConnectionPool
import psycopg2.extras

class Genero:
    def __init__(self, id=None, nombre=None, descripcion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
    
    @staticmethod
    def get_all():
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM genero ORDER BY nombre")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching generos: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def get_by_id(genero_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM genero WHERE id = %s", (genero_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching genero: {e}")
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
                UPDATE genero SET nombre = %s, descripcion = %s, updated_at = CURRENT_TIMESTAMP 
                WHERE id = %s RETURNING *
                """, (self.nombre, self.descripcion, self.id))
            else:
                cursor.execute("""
                INSERT INTO genero (nombre, descripcion) VALUES (%s, %s) RETURNING *
                """, (self.nombre, self.descripcion))
            
            conn.commit()
            return cursor.fetchone()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error saving genero: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def delete(genero_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM genero WHERE id = %s RETURNING id", (genero_id,))
            result = cursor.fetchone()
            conn.commit()
            return result is not None
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error deleting genero: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)