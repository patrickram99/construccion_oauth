from flask import Blueprint, request, jsonify
from backend.models.postgresql_autor_model import AutorModel

autor_blueprint = Blueprint('autor_blueprint', __name__)
autor_model = AutorModel()

@autor_blueprint.route('/autores', methods=['GET'])
def get_all_autores():
    autores = autor_model.get_all_autores()
    return jsonify(autores)

@autor_blueprint.route('/autores/<int:autor_id>', methods=['GET'])
def get_autor_by_id(autor_id):
    autor = autor_model.get_autor_by_id(autor_id)
    if autor:
        return jsonify(autor)
    return jsonify({"message": "Autor no encontrado"}), 404

@autor_blueprint.route('/autores', methods=['POST'])
def create_autor():
    autor_data = request.json
    autor_id = autor_model.create_autor(autor_data)
    return jsonify({"id": autor_id, "message": "Autor creado exitosamente"}), 201

@autor_blueprint.route('/autores/<int:autor_id>', methods=['PUT'])
def update_autor(autor_id):
    autor_data = request.json
    success = autor_model.update_autor(autor_id, autor_data)
    if success:
        return jsonify({"message": "Autor actualizado exitosamente"})
    return jsonify({"message": "Autor no encontrado"}), 404

@autor_blueprint.route('/autores/<int:autor_id>', methods=['DELETE'])
def delete_autor(autor_id):
    success = autor_model.delete_autor(autor_id)
    if success:
        return jsonify({"message": "Autor eliminado exitosamente"})
    return jsonify({"message": "Autor no encontrado"}), 404