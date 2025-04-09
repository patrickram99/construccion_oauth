from flask import Blueprint, request, jsonify
from backend.models.postgresql_genero_model import GeneroModel
from backend.models.postgresql_libro_model import LibroModel

genero_blueprint = Blueprint('genero_blueprint', __name__)
genero_model = GeneroModel()
libro_model = LibroModel()

@genero_blueprint.route('/generos', methods=['GET'])
def get_all_generos():
    # Parámetro opcional para incluir o no los eliminados lógicamente
    incluir_eliminados = request.args.get('incluir_eliminados', 'false').lower() == 'true'
    generos = genero_model.get_all_generos(incluir_eliminados)
    return jsonify(generos)

@genero_blueprint.route('/generos/<int:genero_id>', methods=['GET'])
def get_genero_by_id(genero_id):
    genero = genero_model.get_genero_by_id(genero_id)
    if genero and not genero.get('eliminado', False):
        return jsonify(genero)
    return jsonify({"message": "Género no encontrado o ha sido eliminado"}), 404

@genero_blueprint.route('/generos/codigo/<string:codigo>', methods=['GET'])
def get_genero_by_codigo(codigo):
    genero = genero_model.get_genero_by_codigo(codigo)
    if genero and not genero.get('eliminado', False):
        return jsonify(genero)
    return jsonify({"message": "Género no encontrado o ha sido eliminado"}), 404

@genero_blueprint.route('/generos', methods=['POST'])
def create_genero():
    # Validación de datos obligatorios
    if not request.is_json:
        return jsonify({"message": "El contenido debe ser JSON"}), 400
    
    genero_data = request.json
    
    # Validación de campos requeridos
    if 'codigo' not in genero_data or not genero_data['codigo'].strip():
        return jsonify({"message": "El código del género es obligatorio"}), 400
    
    if 'nombre' not in genero_data or not genero_data['nombre'].strip():
        return jsonify({"message": "El nombre del género es obligatorio"}), 400
    
    # Asegurar que los campos de texto no tengan espacios extra
    genero_data['codigo'] = genero_data['codigo'].strip()
    genero_data['nombre'] = genero_data['nombre'].strip()
    
    # Verificar si el código ya existe
    if genero_model.get_genero_by_codigo(genero_data['codigo']):
        return jsonify({"message": f"Ya existe un género con el código {genero_data['codigo']}"}), 400
    
    try:
        genero_id = genero_model.create_genero(genero_data)
        return jsonify({"id": genero_id, "message": "Género creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"message": f"Error al crear género: {str(e)}"}), 500

@genero_blueprint.route('/generos/<int:genero_id>', methods=['PUT'])
def update_genero(genero_id):
    # Verificar que el género existe y no está eliminado
    genero_existente = genero_model.get_genero_by_id(genero_id)
    if not genero_existente:
        return jsonify({"message": "Género no encontrado"}), 404
    
    if genero_existente.get('eliminado', False):
        return jsonify({"message": "No se puede actualizar un género eliminado"}), 400
    
    # Validación de datos obligatorios
    if not request.is_json:
        return jsonify({"message": "El contenido debe ser JSON"}), 400
    
    genero_data = request.json
    
    # Validación de campos requeridos si están presentes
    if 'codigo' in genero_data and not genero_data['codigo'].strip():
        return jsonify({"message": "El código del género no puede estar vacío"}), 400
    
    if 'nombre' in genero_data and not genero_data['nombre'].strip():
        return jsonify({"message": "El nombre del género no puede estar vacío"}), 400
    
    # Asegurar que los campos de texto no tengan espacios extra
    if 'codigo' in genero_data:
        genero_data['codigo'] = genero_data['codigo'].strip()
    if 'nombre' in genero_data:
        genero_data['nombre'] = genero_data['nombre'].strip()
    
    # Verificar si el código ya existe en otro género
    if 'codigo' in genero_data and genero_data['codigo'] != genero_existente['codigo']:
        genero_con_codigo = genero_model.get_genero_by_codigo(genero_data['codigo'])
        if genero_con_codigo and genero_con_codigo['id'] != genero_id:
            return jsonify({"message": f"Ya existe un género con el código {genero_data['codigo']}"}), 400
    
    try:
        success = genero_model.update_genero(genero_id, genero_data)
        if success:
            return jsonify({"message": "Género actualizado exitosamente"})
        return jsonify({"message": "No se pudo actualizar el género"}), 500
    except Exception as e:
        return jsonify({"message": f"Error al actualizar género: {str(e)}"}), 500

@genero_blueprint.route('/generos/<int:genero_id>', methods=['DELETE'])
def delete_genero(genero_id):
    # Verificar que el género existe y no está eliminado
    genero_existente = genero_model.get_genero_by_id(genero_id)
    if not genero_existente:
        return jsonify({"message": "Género no encontrado"}), 404
    
    if genero_existente.get('eliminado', False):
        return jsonify({"message": "El género ya está eliminado"}), 400
    
    # Verificar si hay libros con este género
    libros_con_genero = libro_model.get_libros_by_genero_codigo(genero_existente['codigo'])
    if libros_con_genero:
        return jsonify({
            "message": f"No se puede eliminar el género porque está siendo utilizado por {len(libros_con_genero)} libro(s)",
            "libros": libros_con_genero
        }), 400
    
    try:
        # Borrado lógico en lugar de físico
        success = genero_model.soft_delete_genero(genero_id)
        if success:
            return jsonify({"message": "Género eliminado exitosamente"})
        return jsonify({"message": "No se pudo eliminar el género"}), 500
    except Exception as e:
        return jsonify({"message": f"Error al eliminar género: {str(e)}"}), 500

@genero_blueprint.route('/generos/<int:genero_id>/libros', methods=['GET'])
def get_libros_by_genero(genero_id):
    # Verificar que el género existe y no está eliminado
    genero_existente = genero_model.get_genero_by_id(genero_id)
    if not genero_existente:
        return jsonify({"message": "Género no encontrado"}), 404
    
    if genero_existente.get('eliminado', False):
        return jsonify({"message": "El género está eliminado"}), 400
    
    try:
        libros = libro_model.get_libros_by_genero_codigo(genero_existente['codigo'])
        return jsonify(libros)
    except Exception as e:
        return jsonify({"message": f"Error al obtener libros del género: {str(e)}"}), 500