from flask import Blueprint, request, jsonify
from models.libro import Libro
from middlewares.auth_middleware import token_required

libro_bp = Blueprint('libro', __name__)

@libro_bp.route('/', methods=['GET'])
@token_required
def get_libros():
    try:
        libros = Libro.get_all()
        return jsonify(libros), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_bp.route('/<int:libro_id>', methods=['GET'])
@token_required
def get_libro(libro_id):
    try:
        libro = Libro.get_by_id(libro_id)
        if libro:
            return jsonify(libro), 200
        return jsonify({"error": "Libro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_bp.route('/', methods=['POST'])
@token_required
def create_libro():
    try:
        data = request.get_json()
        
        if not data or not data.get('titulo'):
            return jsonify({"error": "Se requiere título del libro"}), 400
        
        libro = Libro(
            titulo=data.get('titulo'),
            isbn=data.get('isbn'),
            fecha_publicacion=data.get('fecha_publicacion'),
            descripcion=data.get('descripcion')
        )
        
        result = libro.save()
        
        if result and data.get('autores'):
            for autor_id in data.get('autores'):
                Libro.add_autor(result['id'], autor_id)
        
        if result and data.get('generos'):
            for genero_id in data.get('generos'):
                Libro.add_genero(result['id'], genero_id)
        
        if result:
            return jsonify(Libro.get_by_id(result['id'])), 201
        return jsonify({"error": "Error al crear libro"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# blueprints/libro_blueprint.py (continued)
@libro_bp.route('/<int:libro_id>', methods=['PUT'])
@token_required
def update_libro(libro_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        libro_existente = Libro.get_by_id(libro_id)
        if not libro_existente:
            return jsonify({"error": "Libro no encontrado"}), 404
        
        libro = Libro(
            id=libro_id,
            titulo=data.get('titulo', libro_existente['titulo']),
            isbn=data.get('isbn', libro_existente['isbn']),
            fecha_publicacion=data.get('fecha_publicacion', libro_existente['fecha_publicacion']),
            descripcion=data.get('descripcion', libro_existente['descripcion'])
        )
        
        result = libro.save()
        
        # Update authors if provided
        if result and 'autores' in data:
            # Clear existing relationships
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM libro_autor WHERE libro_id = %s", (libro_id,))
                conn.commit()
                
                # Add new relationships
                for autor_id in data['autores']:
                    Libro.add_autor(libro_id, autor_id)
            except Exception as e:
                conn.rollback()
                print(f"Error updating libro-autor relationships: {e}")
            finally:
                pool.release_connection(conn)
        
        # Update genres if provided
        if result and 'generos' in data:
            # Clear existing relationships
            pool = PostgreSQLConnectionPool.get_instance()
            conn = pool.get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM libro_genero WHERE libro_id = %s", (libro_id,))
                conn.commit()
                
                # Add new relationships
                for genero_id in data['generos']:
                    Libro.add_genero(libro_id, genero_id)
            except Exception as e:
                conn.rollback()
                print(f"Error updating libro-genero relationships: {e}")
            finally:
                pool.release_connection(conn)
        
        if result:
            return jsonify(Libro.get_by_id(libro_id)), 200
        return jsonify({"error": "Error al actualizar libro"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_bp.route('/<int:libro_id>', methods=['DELETE'])
@token_required
def delete_libro(libro_id):
    try:
        if Libro.delete(libro_id):
            return jsonify({"message": "Libro eliminado correctamente"}), 200
        return jsonify({"error": "Libro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_bp.route('/<int:libro_id>/autores/<int:autor_id>', methods=['POST'])
@token_required
def add_autor_to_libro(libro_id, autor_id):
    try:
        if Libro.add_autor(libro_id, autor_id):
            return jsonify({"message": "Autor añadido al libro correctamente"}), 201
        return jsonify({"error": "Error al añadir autor al libro"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_bp.route('/<int:libro_id>/autores/<int:autor_id>', methods=['DELETE'])
@token_required
def remove_autor_from_libro(libro_id, autor_id):
    try:
        if Libro.remove_autor(libro_id, autor_id):
            return jsonify({"message": "Autor eliminado del libro correctamente"}), 200
        return jsonify({"error": "Error al eliminar autor del libro"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_bp.route('/<int:libro_id>/generos/<int:genero_id>', methods=['POST'])
@token_required
def add_genero_to_libro(libro_id, genero_id):
    try:
        if Libro.add_genero(libro_id, genero_id):
            return jsonify({"message": "Género añadido al libro correctamente"}), 201
        return jsonify({"error": "Error al añadir género al libro"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_bp.route('/<int:libro_id>/generos/<int:genero_id>', methods=['DELETE'])
@token_required
def remove_genero_from_libro(libro_id, genero_id):
    try:
        if Libro.remove_genero(libro_id, genero_id):
            return jsonify({"message": "Género eliminado del libro correctamente"}), 200
        return jsonify({"error": "Error al eliminar género del libro"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@libro_bp.route('/por-genero/<int:genero_id>', methods=['GET'])
@token_required
def get_libros_por_genero(genero_id):
    """
    Obtiene todos los libros de un género específico
    """
    try:
        libros = Libro.get_by_genero(genero_id)
        if libros:
            return jsonify(libros), 200
        return jsonify({"message": "No se encontraron libros para este género"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_bp.route('/por-autor/<int:autor_id>', methods=['GET'])
@token_required
def get_libros_por_autor(autor_id):
    """
    Obtiene todos los libros de un autor específico
    """
    try:
        libros = Libro.get_by_autor(autor_id)
        if libros:
            return jsonify(libros), 200
        return jsonify({"message": "No se encontraron libros para este autor"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500