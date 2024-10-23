from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de usuários permitidos
allowed_users = {"usuario1", "usuario2"}

# Endpoint para autenticação
@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json
    username = data.get('username')

    # Verifica se o usuário está na lista de permitidos
    if username in allowed_users:
        return jsonify({"message": "Acesso concedido", "access": True}), 200
    else:
        return jsonify({"message": "Acesso negado", "access": False}), 403

if __name__ == '__main__':
    app.run(debug=True, port=5000)
