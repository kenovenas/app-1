from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações do usuário autorizado
AUTHORIZED_USER = "nome"  # Altere para o nome de usuário desejado

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    username = data.get('username')

    if username == AUTHORIZED_USER:
        # Enviar confirmação para a extensão
        return jsonify({'message': 'Usuário autorizado', 'status': 'success'}), 200
    else:
        return jsonify({'message': 'Usuário não autorizado', 'status': 'error'}), 403

if __name__ == '__main__':
    app.run(debug=True)
