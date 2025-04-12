from flask import Blueprint, request, jsonify
from models.autor import Autor
from middlewares.auth_middleware import token_required

autor_bp = Blueprint('autor', __name__)

@autor_bp.route('/', methods=['GET'])
@token_required
def get_autores():
    try:
        autores = Autor.get_all()
        return jsonify(autores), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@autor_bp.route('/<int:autor_id>', methods=['GET'])
@token_required
def get_autor(autor_id):
    try:
        autor = Autor.get_by_id(autor_id)
        if autor:
            return jsonify(autor), 200
        return jsonify({"error": "Autor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@autor_bp.route('/', methods=['POST'])
@token_required
def create_autor():
    try:
        data = request.get_json()
        
        if not data or not data.get('nombre') or not data.get('apellido'):
            return jsonify({"error": "Se requieren nombre y apellido"}), 400
        
        autor = Autor(
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            nacionalidad=data.get('nacionalidad')
        )
        
        result = autor.save()
        if result:
            return jsonify(result), 201
        return jsonify({"error": "Error al crear autor"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@autor_bp.route('/<int:autor_id>', methods=['PUT'])
@token_required
def update_autor(autor_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        autor_existente = Autor.get_by_id(autor_id)
        if not autor_existente:
            return jsonify({"error": "Autor no encontrado"}), 404
        
        autor = Autor(
            id=autor_id,
            nombre=data.get('nombre', autor_existente['nombre']),
            apellido=data.get('apellido', autor_existente['apellido']),
            fecha_nacimiento=data.get('fecha_nacimiento', autor_existente['fecha_nacimiento']),
            nacionalidad=data.get('nacionalidad', autor_existente['nacionalidad'])
        )
        
        result = autor.save()
        if result:
            return jsonify(result), 200
        return jsonify({"error": "Error al actualizar autor"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@autor_bp.route('/<int:autor_id>', methods=['DELETE'])
@token_required
def delete_autor(autor_id):
    try:
        if Autor.delete(autor_id):
            return jsonify({"message": "Autor eliminado correctamente"}), 200
        return jsonify({"error": "Autor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500