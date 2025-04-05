from flask import Blueprint, request, jsonify
from backend.models.postgresql_libro_model import LibroModel

libro_blueprint = Blueprint('libro_blueprint', __name__)
libro_model = LibroModel()

@libro_blueprint.route('/libros', methods=['GET'])
def get_all_libros():
    libros = libro_model.get_all_libros()
    return jsonify(libros)

@libro_blueprint.route('/libros/<int:libro_id>', methods=['GET'])
def get_libro_by_id(libro_id):
    libro = libro_model.get_libro_by_id(libro_id)
    if libro:
        return jsonify(libro)
    return jsonify({"message": "Libro no encontrado"}), 404

@libro_blueprint.route('/libros', methods=['POST'])
def create_libro():
    libro_data = request.json
    libro_id = libro_model.create_libro(libro_data)
    return jsonify({"id": libro_id, "message": "Libro creado exitosamente"}), 201

@libro_blueprint.route('/libros/<int:libro_id>', methods=['PUT'])
def update_libro(libro_id):
    libro_data = request.json
    success = libro_model.update_libro(libro_id, libro_data)
    if success:
        return jsonify({"message": "Libro actualizado exitosamente"})
    return jsonify({"message": "Libro no encontrado"}), 404

@libro_blueprint.route('/libros/<int:libro_id>', methods=['DELETE'])
def delete_libro(libro_id):
    success = libro_model.delete_libro(libro_id)
    if success:
        return jsonify({"message": "Libro eliminado exitosamente"})
    return jsonify({"message": "Libro no encontrado"}), 404