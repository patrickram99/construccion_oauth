from flask import Blueprint, request, jsonify
from backend.models.postgresql_autor_model import AutorModel
from backend.models.libro_autor_model import LibroAutorModel
from functools import wraps


autor_blueprint = Blueprint('autor_blueprint', __name__)
autor_model = AutorModel()
libro_autor_model = LibroAutorModel()

@autor_blueprint.route('/autores', methods=['GET'])
def get_all_autores():
    # Parámetro opcional para incluir o no los eliminados lógicamente
    incluir_eliminados = request.args.get('incluir_eliminados', 'false').lower() == 'true'
    autores = autor_model.get_all_autores(incluir_eliminados)
    return jsonify(autores)

@autor_blueprint.route('/autores/<int:autor_id>', methods=['GET'])
def get_autor_by_id(autor_id):
    autor = autor_model.get_autor_by_id(autor_id)
    if autor and not autor.get('eliminado', False):
        return jsonify(autor)
    return jsonify({"message": "Autor no encontrado o ha sido eliminado"}), 404

@autor_blueprint.route('/autores', methods=['POST'])
def create_autor():
    # Validación de datos obligatorios
    if not request.is_json:
        return jsonify({"message": "El contenido debe ser JSON"}), 400
    
    autor_data = request.json
    
    # Validación de campos requeridos
    if 'nombre' not in autor_data or not autor_data['nombre'].strip():
        return jsonify({"message": "El nombre del autor es obligatorio"}), 400
    
    if 'apellido' not in autor_data or not autor_data['apellido'].strip():
        return jsonify({"message": "El apellido del autor es obligatorio"}), 400
    
    # Asegurar que los campos de texto no tengan espacios extra
    autor_data['nombre'] = autor_data['nombre'].strip()
    autor_data['apellido'] = autor_data['apellido'].strip()
    
    # Validar formato de fecha si está presente
    if 'fecha_nacimiento' in autor_data and autor_data['fecha_nacimiento']:
        try:
            from datetime import datetime
            datetime.strptime(autor_data['fecha_nacimiento'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "El formato de fecha debe ser YYYY-MM-DD"}), 400
    
    try:
        autor_id = autor_model.create_autor(autor_data)
        return jsonify({"id": autor_id, "message": "Autor creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"message": f"Error al crear autor: {str(e)}"}), 500

@autor_blueprint.route('/autores/<int:autor_id>', methods=['PUT'])
def update_autor(autor_id):
    # Verificar que el autor existe y no está eliminado
    autor_existente = autor_model.get_autor_by_id(autor_id)
    if not autor_existente:
        return jsonify({"message": "Autor no encontrado"}), 404
    
    if autor_existente.get('eliminado', False):
        return jsonify({"message": "No se puede actualizar un autor eliminado"}), 400
    
    # Validación de datos obligatorios
    if not request.is_json:
        return jsonify({"message": "El contenido debe ser JSON"}), 400
    
    autor_data = request.json
    
    # Validación de campos requeridos
    if 'nombre' in autor_data and not autor_data['nombre'].strip():
        return jsonify({"message": "El nombre del autor no puede estar vacío"}), 400
    
    if 'apellido' in autor_data and not autor_data['apellido'].strip():
        return jsonify({"message": "El apellido del autor no puede estar vacío"}), 400
    
    # Asegurar que los campos de texto no tengan espacios extra
    if 'nombre' in autor_data:
        autor_data['nombre'] = autor_data['nombre'].strip()
    if 'apellido' in autor_data:
        autor_data['apellido'] = autor_data['apellido'].strip()
    
    # Validar formato de fecha si está presente
    if 'fecha_nacimiento' in autor_data and autor_data['fecha_nacimiento']:
        try:
            from datetime import datetime
            datetime.strptime(autor_data['fecha_nacimiento'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "El formato de fecha debe ser YYYY-MM-DD"}), 400
    
    try:
        success = autor_model.update_autor(autor_id, autor_data)
        if success:
            return jsonify({"message": "Autor actualizado exitosamente"})
        return jsonify({"message": "No se pudo actualizar el autor"}), 500
    except Exception as e:
        return jsonify({"message": f"Error al actualizar autor: {str(e)}"}), 500

@autor_blueprint.route('/autores/<int:autor_id>', methods=['DELETE'])
def delete_autor(autor_id):
    # Verificar que el autor existe y no está eliminado
    autor_existente = autor_model.get_autor_by_id(autor_id)
    if not autor_existente:
        return jsonify({"message": "Autor no encontrado"}), 404
    
    if autor_existente.get('eliminado', False):
        return jsonify({"message": "El autor ya está eliminado"}), 400
    
    try:
        # Borrado lógico en lugar de físico
        success = autor_model.soft_delete_autor(autor_id)
        if success:
            return jsonify({"message": "Autor eliminado exitosamente"})
        return jsonify({"message": "No se pudo eliminar el autor"}), 500
    except Exception as e:
        return jsonify({"message": f"Error al eliminar autor: {str(e)}"}), 500

@autor_blueprint.route('/autores/<int:autor_id>/libros', methods=['GET'])
def get_libros_by_autor(autor_id):
    # Verificar que el autor existe y no está eliminado
    autor_existente = autor_model.get_autor_by_id(autor_id)
    if not autor_existente:
        return jsonify({"message": "Autor no encontrado"}), 404
    
    if autor_existente.get('eliminado', False):
        return jsonify({"message": "El autor está eliminado"}), 400
    
    try:
        libros = libro_autor_model.get_libros_by_autor_id(autor_id)
        return jsonify(libros)
    except Exception as e:
        return jsonify({"message": f"Error al obtener libros del autor: {str(e)}"}), 500