def create_tables():
    pool = None
    conn = None
    cursor = None
    
    try:
        from db.connection_pool import PostgreSQLConnectionPool
        pool = PostgreSQLConnectionPool.get_instance()
        conn = pool.get_connection()
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS autor (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            fecha_nacimiento DATE,
            nacionalidad VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS genero (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL UNIQUE,
            descripcion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libro (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            isbn VARCHAR(20) UNIQUE,
            fecha_publicacion DATE,
            descripcion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create bridge tables for many-to-many relationships
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libro_autor (
            libro_id INTEGER REFERENCES libro(id) ON DELETE CASCADE,
            autor_id INTEGER REFERENCES autor(id) ON DELETE CASCADE,
            PRIMARY KEY (libro_id, autor_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libro_genero (
            libro_id INTEGER REFERENCES libro(id) ON DELETE CASCADE,
            genero_id INTEGER REFERENCES genero(id) ON DELETE CASCADE,
            PRIMARY KEY (libro_id, genero_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        print("Tables created successfully")
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error creating tables: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and pool:
            pool.release_connection(conn)

if __name__ == "__main__":
    create_tables()