from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de usuários permitidos
valid_users = ['user1', 'user2', 'user3']  # Adicione os nomes dos usuários permitidos

# Rota para autenticar o usuário
@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    username = data.get('username')

    # Verifica se o usuário está na lista de usuários permitidos
    if username in valid_users:
        token = f"{username}-token"  # Simula um token baseado no nome do usuário
        return jsonify({'success': True, 'token': token})
    else:
        return jsonify({'success': False, 'message': 'Usuário não autorizado'}), 401

# Rota para verificar o token
@app.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.json
    token = data.get('token')

    # Simula a validação do token
    if token in [f'{user}-token' for user in valid_users]:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Token inválido'}), 401

if __name__ == '__main__':
    app.run(debug=True)
