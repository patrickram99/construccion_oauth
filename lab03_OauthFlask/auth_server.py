from flask import Flask, request, jsonify
import jwt
import datetime
import uuid

app = Flask(__name__)

# En una aplicación real, almacenar estos datos de forma segura
CLIENT_ID = "test_client"
CLIENT_SECRET = "test_secret"
JWT_SECRET = "mi_clave_super_secreta"

@app.route('/token', methods=['POST'])
def token():
    data = request.get_json()
    
    # Validación simple
    if not data or data.get('client_id') != CLIENT_ID or data.get('client_secret') != CLIENT_SECRET:
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

if __name__ == '__main__':
    app.run(port=8080, debug=True)