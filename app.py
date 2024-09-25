from flask import Flask, request, jsonify, render_template_string
import secrets
import time
import json
import os

app = Flask(__name__)
application = app

# Arquivo para armazenar os acessos dos usuários
ACESSOS_FILE = "acessos.json"

# Carrega os acessos dos usuários de um arquivo JSON
def load_access_data():
    if os.path.exists(ACESSOS_FILE):
        with open(ACESSOS_FILE, "r") as file:
            return json.load(file)
    return {}

# Salva os acessos dos usuários em um arquivo JSON
def save_access_data(data):
    with open(ACESSOS_FILE, "w") as file:
        json.dump(data, file)

# Carrega os dados de acessos ao iniciar o servidor
user_access_history = load_access_data()

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

# Função para garantir que o histórico de usuários seja mantido
def sync_user_data(allowed_users_template):
    for user, data in allowed_users_template.items():
        if user not in user_access_history:
            # Se o usuário não estiver no histórico, adicionamos
            user_access_history[user] = {"visits": 0, "max_visits": data["max_visits"]}
    # Remover usuários do histórico que não estão mais na lista de permitidos
    for user in list(user_access_history.keys()):
        if user not in allowed_users_template:
            del user_access_history[user]

@app.route('/', methods=['GET', 'POST'])
def home():
    # Template de usuários permitidos (isso pode ser movido para um banco de dados)
    allowed_users_template = {
        "usuario1": {"max_visits": 10},
        "usuario2": {"max_visits": 5},
        "usuario_configurado": {"max_visits": 10}
    }
    
    # Sincroniza os dados dos usuários com o histórico antes de processar qualquer solicitação
    sync_user_data(allowed_users_template)
    save_access_data(user_access_history)  # Salva o histórico sincronizado

    if request.method == 'POST':
        username = request.form.get('username')
        if username in user_access_history:  # Verifica se o usuário está no histórico de acessos
            user_data = user_access_history[username]

            # Verifica se o usuário já excedeu o número máximo de acessos
            if user_data["visits"] >= user_data["max_visits"]:
                return render_template_string(f'''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Acesso Negado</title>
                    </head>
                    <body>
                        <h1>Acesso Negado</h1>
                        <p>Você atingiu o limite máximo de acessos.</p>
                    </body>
                    </html>
                ''')

            # Incrementa o número de acessos do usuário
            user_data["visits"] += 1
            save_access_data(user_access_history)  # Salva a contagem de acessos

            # Gera uma nova chave se a anterior estiver expirada
            if "key_data" not in user_data or not is_key_valid(user_data["key_data"]):
                user_data["key_data"] = {
                    "key": generate_key(),
                    "timestamp": time.time()
                }
                save_access_data(user_access_history)  # Salva a chave gerada

            # Exibe a chave e as informações de acesso
            return render_template_string(f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Access Key</title>
                <style>
                    body {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        position: relative;
                        flex-direction: column;
                    }}
                    .content {{
                        text-align: center;
                        margin-top: 20px;
                    }}
                    .author {{
                        position: absolute;
                        top: 10px;
                        left: 10px;
                        color: #000;
                        font-size: 18px;
                    }}
                    .banner-telegram {{
                        position: absolute;
                        top: 10px;
                        right: 10px;
                        background-color: #0088cc;
                        padding: 10px;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    }}
                    .banner-telegram a {{
                        color: #ffcc00;
                        text-decoration: none;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="author">Autor = Keno Venas</div>
                <div class="banner-telegram">
                    <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Grupo do Telegram</a>
                </div>
                <div class="content">
                    <h1>Access Key</h1>
                    <p>Chave: {user_data["key_data"]["key"]}</p>
                    <p>Acessos Realizados: {user_data["visits"]} de {user_data["max_visits"]}</p>
                </div>
            </body>
            </html>
            ''')

        else:
            return "Acesso negado"

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            .telegram-button {{
                background-color: #0088cc;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin-top: 20px;
                cursor: pointer;
            }}
            .telegram-button:hover {{
                background-color: #005f99;
            }}
        </style>
    </head>
    <body>
        <h1>Digite seu usuário</h1>
        <form method="POST">
            <input type="text" name="username" required>
            <button type="submit">Acessar</button>
        </form>
        <p>Entrar em contato para ter acesso:</p>
        <a href="https://t.me/Keno_venas" target="_blank" class="telegram-button">Keno Venas</a>
    </body>
    </html>
    '''

@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.get_json()
    if 'key' in data:
        for user, user_data in user_access_history.items():
            if data['key'] == user_data['key_data']['key'] and is_key_valid(user_data["key_data"]):
                return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
