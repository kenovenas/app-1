from flask import Flask, request, jsonify, render_template_string
import secrets
import time
import json
import os

app = Flask(__name__)

# Nome dos arquivos para usuários e acessos
USUARIOS_FILE = 'usuarios.txt'
ACESSOS_FILE = 'acessos.json'

# Limite máximo de acessos por usuário
max_access = 5

# Função para carregar usuários de um arquivo
def load_users():
    if not os.path.exists(USUARIOS_FILE):
        return []
    with open(USUARIOS_FILE, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Função para carregar acessos de um arquivo
def load_accesses():
    if not os.path.exists(ACESSOS_FILE):
        return {}
    with open(ACESSOS_FILE, 'r') as f:
        return json.load(f)

# Função para salvar acessos em um arquivo
def save_accesses(access_data):
    with open(ACESSOS_FILE, 'w') as f:
        json.dump(access_data, f)

# Função para gerar uma chave aleatória
def generate_key():
    return secrets.token_hex(16)  # Gera uma chave hexadecimal de 16 bytes

# Função para verificar se a chave ainda é válida
def is_key_valid(key_data):
    if key_data["key"] and key_data["timestamp"]:
        current_time = time.time()
        # Verifica se a chave ainda é válida (5 minutos = 300 segundos)
        if current_time - key_data["timestamp"] <= 300:
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def home():
    users = load_users()
    access_data = load_accesses()

    if request.method == 'POST':
        username = request.form.get('username')
        if username in users:  # Verifica se o usuário está na lista permitida
            user_access_count = access_data.get(username, 0)
            if user_access_count < max_access:  # Verifica se o usuário atingiu o limite de acessos
                key_data = {"key": generate_key(), "timestamp": time.time()}

                access_data[username] = user_access_count + 1  # Incrementa a contagem de acessos do usuário
                save_accesses(access_data)  # Salva o novo estado de acessos

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
                    <p>Acesso realizado: {access_data[username]}/{max_access}</p>
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
