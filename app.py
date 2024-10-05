from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lista de usuários permitidos
allowed_users = ["user1", "user2", "kenovenas"]  # Insira os usuários permitidos aqui

# Rota para a autenticação do usuário
@app.route('/login', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    if username in allowed_users:
        return jsonify({"authenticated": True}), 200
    else:
        return jsonify({"authenticated": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
