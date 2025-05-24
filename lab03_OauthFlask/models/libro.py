from db.connection_pool import PostgreSQLConnectionPool
import psycopg2.extras

class Libro:
    def __init__(self, id=None, titulo=None, isbn=None, fecha_publicacion=None, descripcion=None):
        self.id = id
        self.titulo = titulo
        self.isbn = isbn
        self.fecha_publicacion = fecha_publicacion
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
            
            cursor.execute("SELECT * FROM libro ORDER BY titulo")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching libros: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def get_by_id(libro_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("SELECT * FROM libro WHERE id = %s", (libro_id,))
            libro = cursor.fetchone()
            
            if libro:
                # Fetch autores
                cursor.execute("""
                SELECT a.* FROM autor a
                JOIN libro_autor la ON a.id = la.autor_id
                WHERE la.libro_id = %s
                """, (libro_id,))
                libro['autores'] = cursor.fetchall()
                
                # Fetch generos
                cursor.execute("""
                SELECT g.* FROM genero g
                JOIN libro_genero lg ON g.id = lg.genero_id
                WHERE lg.libro_id = %s
                """, (libro_id,))
                libro['generos'] = cursor.fetchall()
            
            return libro
        except Exception as e:
            print(f"Error fetching libro: {e}")
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
                UPDATE libro SET titulo = %s, isbn = %s, fecha_publicacion = %s, descripcion = %s, 
                updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *
                """, (self.titulo, self.isbn, self.fecha_publicacion, self.descripcion, self.id))
            else:
                cursor.execute("""
                INSERT INTO libro (titulo, isbn, fecha_publicacion, descripcion) 
                VALUES (%s, %s, %s, %s) RETURNING *
                """, (self.titulo, self.isbn, self.fecha_publicacion, self.descripcion))
            
            conn.commit()
            return cursor.fetchone()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error saving libro: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def delete(libro_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM libro WHERE id = %s RETURNING id", (libro_id,))
            result = cursor.fetchone()
            conn.commit()
            return result is not None
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error deleting libro: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def add_autor(libro_id, autor_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO libro_autor (libro_id, autor_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", 
                          (libro_id, autor_id))
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error adding autor to libro: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def remove_autor(libro_id, autor_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM libro_autor WHERE libro_id = %s AND autor_id = %s", 
                          (libro_id, autor_id))
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error removing autor from libro: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def add_genero(libro_id, genero_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO libro_genero (libro_id, genero_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", 
                          (libro_id, genero_id))
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error adding genero to libro: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)
    
    @staticmethod
    def remove_genero(libro_id, genero_id):
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM libro_genero WHERE libro_id = %s AND genero_id = %s", 
                          (libro_id, genero_id))
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error removing genero from libro: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)

    @staticmethod
    def get_by_genero(genero_id):
        """
        Obtiene todos los libros de un género específico
        """
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Primero obtenemos los IDs de libros que pertenecen al género
            cursor.execute("""
                SELECT libro_id FROM libro_genero WHERE genero_id = %s
            """, (genero_id,))
            libro_ids = [row['libro_id'] for row in cursor.fetchall()]
            
            if not libro_ids:
                return []
            
            # Construir la consulta IN de forma segura
            placeholders = ','.join(['%s'] * len(libro_ids))
            query = f"""
                SELECT * FROM libro 
                WHERE id IN ({placeholders})
                ORDER BY titulo
            """
            
            cursor.execute(query, libro_ids)
            libros = cursor.fetchall()
            
            # Para cada libro, obtener sus autores y géneros
            for libro in libros:
                # Fetch autores
                cursor.execute("""
                    SELECT a.* FROM autor a
                    JOIN libro_autor la ON a.id = la.autor_id
                    WHERE la.libro_id = %s
                """, (libro['id'],))
                libro['autores'] = cursor.fetchall()
                
                # Fetch generos
                cursor.execute("""
                    SELECT g.* FROM genero g
                    JOIN libro_genero lg ON g.id = lg.genero_id
                    WHERE lg.libro_id = %s
                """, (libro['id'],))
                libro['generos'] = cursor.fetchall()
            
            return libros
        except Exception as e:
            print(f"Error getting books by genre: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)

    @staticmethod
    def get_by_autor(autor_id):
        """
        Obtiene todos los libros de un autor específico
        """
        pool = None
        conn = None
        cursor = None
        
        try:
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Primero obtenemos los IDs de libros que pertenecen al autor
            cursor.execute("""
                SELECT libro_id FROM libro_autor WHERE autor_id = %s
            """, (autor_id,))
            libro_ids = [row['libro_id'] for row in cursor.fetchall()]
            
            if not libro_ids:
                return []
            
            # Construir la consulta IN de forma segura
            placeholders = ','.join(['%s'] * len(libro_ids))
            query = f"""
                SELECT * FROM libro 
                WHERE id IN ({placeholders})
                ORDER BY titulo
            """
            
            cursor.execute(query, libro_ids)
            libros = cursor.fetchall()
            
            # Para cada libro, obtener sus autores y géneros
            for libro in libros:
                # Fetch autores
                cursor.execute("""
                    SELECT a.* FROM autor a
                    JOIN libro_autor la ON a.id = la.autor_id
                    WHERE la.libro_id = %s
                """, (libro['id'],))
                libro['autores'] = cursor.fetchall()
                
                # Fetch generos
                cursor.execute("""
                    SELECT g.* FROM genero g
                    JOIN libro_genero lg ON g.id = lg.genero_id
                    WHERE lg.libro_id = %s
                """, (libro['id'],))
                libro['generos'] = cursor.fetchall()
            
            return libros
        except Exception as e:
            print(f"Error getting books by author: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and pool:
                pool.release_connection(conn)