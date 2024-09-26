from flask import Flask, request, jsonify, render_template_string
import secrets
import os
import acessos  # Importa o módulo de acessos

app = Flask(__name__)

USUARIOS_FILE = 'usuarios.txt'
MAX_ACESSOS = 5

# Função para carregar usuários de um arquivo
def load_users():
    if not os.path.exists(USUARIOS_FILE):
        return []
    with open(USUARIOS_FILE, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Função para gerar uma chave aleatória
def generate_key():
    return secrets.token_hex(16)  # Gera uma chave hexadecimal de 16 bytes

@app.route('/', methods=['GET', 'POST'])
def home():
    users = load_users()  # Carrega os usuários permitidos
    access_data = acessos.load_accesses()  # Carrega a contagem de acessos

    if request.method == 'POST':
        username = request.form.get('username')

        if username in users:  # Verifica se o usuário está na lista permitida
            user_access_count = access_data.get(username, 0)  # Obtém a contagem atual de acessos
            
            if user_access_count < MAX_ACESSOS:  # Verifica se o usuário atingiu o limite de acessos
                key_data = {"key": generate_key()}

                # Atualiza a contagem de acessos do usuário
                acessos.update_access(username)

                return render_template_string(f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Access Key</title>
                </head>
                <body>
                    <h1>Access Key</h1>
                    <p>{key_data["key"]}</p>
                    <p>Acesso realizado: {access_data[username] + 1}/{MAX_ACESSOS}</p>
                </body>
                </html>
                ''')

            else:
                return "Limite de acessos atingido. Acesso negado."

        else:
            return "Acesso negado"

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
    </head>
    <body>
        <h1>Digite seu usuário</h1>
        <form method="POST">
            <input type="text" name="username" required>
            <button type="submit">Acessar</button>
        </form>
    </body>
    </html>
    '''

@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.get_json()
    if 'key' in data:
        # O código para validar a chave pode ser adicionado aqui
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
