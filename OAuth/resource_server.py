from flask import Flask, request, jsonify
from functools import wraps
import jwt
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# URL de la base de datos (configurar en el entorno o reemplazar directamente)
DATABASE_URL = "XDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"

# La misma clave secreta que el servidor de autenticación
JWT_SECRET = "mi_clave_super_secreta"

# Conexión a la base de datos
def obtener_conexion_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn

# Crear tabla si no existe
def inicializar_db():
    conn = obtener_conexion_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Decorador para validación de token
def token_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        token = None
        
        # Extraer token del encabezado de Autorización
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({"error": "token_faltante"}), 401
        
        # Verificar token
        try:
            jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except:
            return jsonify({"error": "token_invalido"}), 401
        
        return f(*args, **kwargs)
    
    return decorada

# Endpoints CRUD
@app.route('/api/productos', methods=['GET'])
@token_requerido
def obtener_productos():
    conn = obtener_conexion_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM productos')
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(productos)

@app.route('/api/productos/<int:id>', methods=['GET'])
@token_requerido
def obtener_producto(id):
    conn = obtener_conexion_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM productos WHERE id = %s', (id,))
    producto = cur.fetchone()
    cur.close()
    conn.close()
    
    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    return jsonify(producto)

@app.route('/api/productos', methods=['POST'])
@token_requerido
def crear_producto():
    data = request.get_json()
    
    if not data or not data.get('nombre'):
        return jsonify({"error": "El nombre es obligatorio"}), 400
    
    conn = obtener_conexion_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        'INSERT INTO productos (nombre, descripcion) VALUES (%s, %s) RETURNING *',
        (data['nombre'], data.get('descripcion', ''))
    )
    nuevo_producto = cur.fetchone()
    cur.close()
    conn.close()
    
    return jsonify(nuevo_producto), 201

@app.route('/api/productos/<int:id>', methods=['PUT'])
@token_requerido
def actualizar_producto(id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    conn = obtener_conexion_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Verificar si el producto existe
    cur.execute('SELECT * FROM productos WHERE id = %s', (id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404
    
    # Actualizar producto
    cur.execute(
        'UPDATE productos SET nombre = %s, descripcion = %s WHERE id = %s RETURNING *',
        (data.get('nombre'), data.get('descripcion'), id)
    )
    producto_actualizado = cur.fetchone()
    cur.close()
    conn.close()
    
    return jsonify(producto_actualizado)

@app.route('/api/productos/<int:id>', methods=['DELETE'])
@token_requerido
def eliminar_producto(id):
    conn = obtener_conexion_db()
    cur = conn.cursor()
    
    # Verificar si el producto existe
    cur.execute('SELECT * FROM productos WHERE id = %s', (id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404
    
    # Eliminar producto
    cur.execute('DELETE FROM productos WHERE id = %s', (id,))
    cur.close()
    conn.close()
    
    return jsonify({"mensaje": f"Producto {id} eliminado con éxito"})

if __name__ == '__main__':
    inicializar_db()
    app.run(port=5001, debug=True)