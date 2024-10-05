from flask import Flask, request, jsonify
from flask_cors import CORS

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
