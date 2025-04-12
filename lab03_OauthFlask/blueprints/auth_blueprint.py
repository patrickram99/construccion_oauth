from flask import Blueprint, request, jsonify
import jwt
import datetime
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

auth_bp = Blueprint('auth', __name__)

# En una aplicación real, almacenar estos datos de forma segura
CLIENT_ID = os.getenv("CLIENT_ID", "test_client")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "test_secret")
JWT_SECRET = os.getenv("JWT_SECRET", "mi_clave_super_secreta")

@auth_bp.route('/token', methods=['POST'])
def token():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        # Validación simple
        if data.get('client_id') != CLIENT_ID or data.get('client_secret') != CLIENT_SECRET:
            return jsonify({"error": "cliente_invalido"}), 401
        
        # Crear token JWT
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        payload = {
            "sub": CLIENT_ID,
            "exp": expiration,
            "jti": str(uuid.uuid4())
        }
        
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            "token_acceso": token,
            "tipo_token": "bearer",
            "expira_en": 3600
        })
    except Exception as e:
        return jsonify({"error": f"Error al generar token: {str(e)}"}), 500