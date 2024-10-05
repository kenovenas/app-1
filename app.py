from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de usuários autorizados (substitua com seu armazenamento preferido)
usuarios_autorizados = {"usuario1", "usuario2", "usuario3"}

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    usuario = data.get('usuario')

    if usuario in usuarios_autorizados:
        return jsonify({"autorizado": True}), 200
    else:
        return jsonify({"autorizado": False}), 200

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)
CORS(app)  # Permite chamadas de qualquer origem

# Lista de usuários autorizados (exemplo)
allowed_users = ["usuario1", "usuario2", "usuario3"]  # Adicione os usuários autorizados aqui

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get('username')

    if username in allowed_users:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Usuário não autorizado!"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Altere a porta se necessário
