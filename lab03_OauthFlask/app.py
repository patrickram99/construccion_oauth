from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from blueprints.libro_blueprint import libro_bp
from blueprints.autor_blueprint import autor_bp
from blueprints.genero_blueprint import genero_bp
from blueprints.auth_blueprint import auth_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    app.register_blueprint(libro_bp, url_prefix='/api/libros')
    app.register_blueprint(autor_bp, url_prefix='/api/autores')
    app.register_blueprint(genero_bp, url_prefix='/api/generos')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)