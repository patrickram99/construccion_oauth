from flask import Blueprint, request, jsonify
from models.genero import Genero
from middlewares.auth_middleware import token_required

genero_bp = Blueprint('genero', __name__)

@genero_bp.route('/', methods=['GET'])
@token_required
def get_generos():
    try:
        generos = Genero.get_all()
        return jsonify(generos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genero_bp.route('/<int:genero_id>', methods=['GET'])
@token_required
def get_genero(genero_id):
    try:
        genero = Genero.get_by_id(genero_id)
        if genero:
            return jsonify(genero), 200
        return jsonify({"error": "Género no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genero_bp.route('/', methods=['POST'])
@token_required
def create_genero():
    try:
        data = request.get_json()
        
        if not data or not data.get('nombre'):
            return jsonify({"error": "Se requiere nombre del género"}), 400
        
        genero = Genero(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion')
        )
        
        result = genero.save()
        if result:
            return jsonify(result), 201
        return jsonify({"error": "Error al crear género"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genero_bp.route('/<int:genero_id>', methods=['PUT'])
@token_required
def update_genero(genero_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        genero_existente = Genero.get_by_id(genero_id)
        if not genero_existente:
            return jsonify({"error": "Género no encontrado"}), 404
        
        genero = Genero(
            id=genero_id,
            nombre=data.get('nombre', genero_existente['nombre']),
            descripcion=data.get('descripcion', genero_existente['descripcion'])
        )
        
        result = genero.save()
        if result:
            return jsonify(result), 200
        return jsonify({"error": "Error al actualizar género"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genero_bp.route('/<int:genero_id>', methods=['DELETE'])
@token_required
def delete_genero(genero_id):
    try:
        if Genero.delete(genero_id):
            return jsonify({"message": "Género eliminado correctamente"}), 200
        return jsonify({"error": "Género no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500