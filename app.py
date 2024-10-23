from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações do usuário autorizado
AUTHORIZED_USER = "nome_do_usuario"  # Altere para o nome de usuário desejado

@app.route('/authorize', methods=['POST'])
def authorize():
    data = request.get_json()
    username = data.get('username')

    if username == AUTHORIZED_USER:
        # Enviar confirmação para a extensão
        return jsonify({'message': 'Usuário autorizado', 'status': 'success'}), 200
    else:
        return jsonify({'message': 'Usuário não autorizado', 'status': 'error'}), 403

if __name__ == '__main__':
    app.run(debug=True)
