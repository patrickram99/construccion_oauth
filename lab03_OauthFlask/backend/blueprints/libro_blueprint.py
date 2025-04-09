from flask import Blueprint, request, jsonify
from backend.models.postgresql_libro_model import LibroModel
from backend.models.postgresql_autor_model import AutorModel
from backend.models.postgresql_genero_model import GeneroModel
from backend.models.libro_autor_model import LibroAutorModel

libro_blueprint = Blueprint('libro_blueprint', __name__)
libro_model = LibroModel()
autor_model = AutorModel()
genero_model = GeneroModel()
libro_autor_model = LibroAutorModel()

@libro_blueprint.route('/libros', methods=['GET'])
def get_all_libros():
    # Parámetro opcional para incluir o no los eliminados lógicamente
    incluir_eliminados = request.args.get('incluir_eliminados', 'false').lower() == 'true'
    libros = libro_model.get_all_libros(incluir_eliminados)
    return jsonify(libros)

@libro_blueprint.route('/libros/<int:libro_id>', methods=['GET'])
def get_libro_by_id(libro_id):
    libro = libro_model.get_libro_by_id(libro_id)
    if libro and not libro.get('eliminado', False):
        return jsonify(libro)
    return jsonify({"message": "Libro no encontrado o ha sido eliminado"}), 404

@libro_blueprint.route('/libros', methods=['POST'])
def create_libro():
    # Validación de datos obligatorios
    if not request.is_json:
        return jsonify({"message": "El contenido debe ser JSON"}), 400
    
    libro_data = request.json
    
    # Validación de campos requeridos
    if 'titulo' not in libro_data or not libro_data['titulo'].strip():
        return jsonify({"message": "El título del libro es obligatorio"}), 400
    
    # Asegurar que los campos de texto no tengan espacios extra
    libro_data['titulo'] = libro_data['titulo'].strip()
    
    # Validar que el género existe si se proporciona
    if 'genero_codigo' in libro_data and libro_data['genero_codigo']:
        genero = genero_model.get_genero_by_codigo(libro_data['genero_codigo'])
        if not genero:
            return jsonify({"message": f"El género con código {libro_data['genero_codigo']} no existe"}), 400
    
    # Validar que los autores existen si se proporcionan
    if 'autores' in libro_data and libro_data['autores']:
        for autor_id in libro_data['autores']:
            autor = autor_model.get_autor_by_id(autor_id)
            if not autor:
                return jsonify({"message": f"El autor con ID {autor_id} no existe"}), 400
            if autor.get('eliminado', False):
                return jsonify({"message": f"El autor con ID {autor_id} está marcado como eliminado"}), 400
    
    # Validar el ISBN si se proporciona
    if 'isbn' in libro_data and libro_data['isbn']:
        # Verificar si el ISBN ya existe
        if libro_model.get_libro_by_isbn(libro_data['isbn']):
            return jsonify({"message": f"Ya existe un libro con el ISBN {libro_data['isbn']}"}), 400
        
        # Validar formato de ISBN (ejemplo simple)
        isbn = libro_data['isbn'].replace('-', '').replace(' ', '')
        if not (len(isbn) == 10 or len(isbn) == 13):
            return jsonify({"message": "El ISBN debe tener 10 o 13 dígitos"}), 400
    
    try:
        libro_id = libro_model.create_libro(libro_data)
        return jsonify({"id": libro_id, "message": "Libro creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"message": f"Error al crear libro: {str(e)}"}), 500

@libro_blueprint.route('/libros/<int:libro_id>', methods=['PUT'])
def update_libro(libro_id):
    # Verificar que el libro existe y no está eliminado
    libro_existente = libro_model.get_libro_by_id(libro_id)
    if not libro_existente:
        return jsonify({"message": "Libro no encontrado"}), 404
    
    if libro_existente.get('eliminado', False):
        return jsonify({"message": "No se puede actualizar un libro eliminado"}), 400
    
    # Validación de datos obligatorios
    if not request.is_json:
        return jsonify({"message": "El contenido debe ser JSON"}), 400
    
    libro_data = request.json
    
    # Validación de campos requeridos
    if 'titulo' in libro_data and not libro_data['titulo'].strip():
        return jsonify({"message": "El título del libro no puede estar vacío"}), 400
    
    # Asegurar que los campos de texto no tengan espacios extra
    if 'titulo' in libro_data:
        libro_data['titulo'] = libro_data['titulo'].strip()
    
    # Validar que el género existe si se proporciona
    if 'genero_codigo' in libro_data and libro_data['genero_codigo']:
        genero = genero_model.get_genero_by_codigo(libro_data['genero_codigo'])
        if not genero:
            return jsonify({"message": f"El género con código {libro_data['genero_codigo']} no existe"}), 400
    
    # Validar que los autores existen si se proporcionan
    if 'autores' in libro_data and libro_data['autores']:
        for autor_id in libro_data['autores']:
            autor = autor_model.get_autor_by_id(autor_id)
            if not autor:
                return jsonify({"message": f"El autor con ID {autor_id} no existe"}), 400
            if autor.get('eliminado', False):
                return jsonify({"message": f"El autor con ID {autor_id} está marcado como eliminado"}), 400
    
    # Validar el ISBN si se modifica
    if 'isbn' in libro_data and libro_data['isbn'] and libro_data['isbn'] != libro_existente.get('isbn'):
        # Verificar si el ISBN ya existe en otro libro
        libro_con_isbn = libro_model.get_libro_by_isbn(libro_data['isbn'])
        if libro_con_isbn and libro_con_isbn['id'] != libro_id:
            return jsonify({"message": f"Ya existe un libro con el ISBN {libro_data['isbn']}"}), 400
        
        # Validar formato de ISBN (ejemplo simple)
        isbn = libro_data['isbn'].replace('-', '').replace(' ', '')
        if not (len(isbn) == 10 or len(isbn) == 13):
            return jsonify({"message": "El ISBN debe tener 10 o 13 dígitos"}), 400
    
    try:
        success = libro_model.update_libro(libro_id, libro_data)
        if success:
            return jsonify({"message": "Libro actualizado exitosamente"})
        return jsonify({"message": "No se pudo actualizar el libro"}), 500
    except Exception as e:
        return jsonify({"message": f"Error al actualizar libro: {str(e)}"}), 500

@libro_blueprint.route('/libros/<int:libro_id>', methods=['DELETE'])
def delete_libro(libro_id):
    # Verificar que el libro existe y no está eliminado
    libro_existente = libro_model.get_libro_by_id(libro_id)
    if not libro_existente:
        return jsonify({"message": "Libro no encontrado"}), 404
    
    if libro_existente.get('eliminado', False):
        return jsonify({"message": "El libro ya está eliminado"}), 400
    
    try:
        # Borrado lógico en lugar de físico
        success = libro_model.soft_delete_libro(libro_id)
        if success:
            return jsonify({"message": "Libro eliminado exitosamente"})
        return jsonify({"message": "No se pudo eliminar el libro"}), 500
    except Exception as e:
        return jsonify({"message": f"Error al eliminar libro: {str(e)}"}), 500

@libro_blueprint.route('/libros/<int:libro_id>/autores', methods=['GET'])
def get_autores_by_libro(libro_id):
    # Verificar que el libro existe y no está eliminado
    libro_existente = libro_model.get_libro_by_id(libro_id)
    if not libro_existente:
        return jsonify({"message": "Libro no encontrado"}), 404
    
    if libro_existente.get('eliminado', False):
        return jsonify({"message": "El libro está eliminado"}), 400
    
    try:
        autores = libro_autor_model.get_autores_by_libro_id(libro_id)
        return jsonify(autores)
    except Exception as e:
        return jsonify({"message": f"Error al obtener autores del libro: {str(e)}"}), 500

@libro_blueprint.route('/libros/<int:libro_id>/autores/<int:autor_id>', methods=['POST'])
def asignar_autor_a_libro(libro_id, autor_id):
    # Verificar que el libro existe y no está eliminado
    libro_existente = libro_model.get_libro_by_id(libro_id)
    if not libro_existente:
        return jsonify({"message": "Libro no encontrado"}), 404
    
    if libro_existente.get('eliminado', False):
        return jsonify({"message": "El libro está eliminado"}), 400
    
    # Verificar que el autor existe y no está eliminado
    autor_existente = autor_model.get_autor_by_id(autor_id)
    if not autor_existente:
        return jsonify({"message": "Autor no encontrado"}), 404
    
    if autor_existente.get('eliminado', False):
        return jsonify({"message": "El autor está eliminado"}), 400
    
    # Obtener datos opcionales
    data = request.json or {}
    orden = data.get('orden', 1)
    rol = data.get('rol', 'Autor principal')
    
    try:
        libro_autor_model.asignar_autor_a_libro(libro_id, autor_id, orden, rol)
        return jsonify({"message": "Autor asignado al libro exitosamente"}), 201
    except Exception as e:
        return jsonify({"message": f"Error al asignar autor al libro: {str(e)}"}), 500

@libro_blueprint.route('/libros/<int:libro_id>/autores/<int:autor_id>', methods=['DELETE'])
def eliminar_autor_de_libro(libro_id, autor_id):
    try:
        success = libro_autor_model.eliminar_autor_de_libro(libro_id, autor_id)
        if success:
            return jsonify({"message": "Autor eliminado del libro exitosamente"})
        return jsonify({"message": "Autor no asignado a este libro"}), 404
    except Exception as e:
        return jsonify({"message": f"Error al eliminar autor del libro: {str(e)}"}), 500