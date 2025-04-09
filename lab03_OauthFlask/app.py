from flask import Flask
from backend.blueprints.autor_blueprint import autor_blueprint
from backend.blueprints.libro_blueprint import libro_blueprint
from backend.blueprints.genero_blueprint import genero_blueprint
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(autor_blueprint)
app.register_blueprint(libro_blueprint)
app.register_blueprint(genero_blueprint)

# Ruta de prueba
@app.route('/')
def index():
    return {"message": "API de gestión de libros y autores"}

if __name__ == '__main__':
    app.run(debug=True)