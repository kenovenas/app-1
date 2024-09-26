from flask import Flask, request, jsonify, render_template_string
import secrets
import time

app = Flask(__name__)
application = app

# Armazenamento para chave, timestamp e usuários permitidos
key_data = {
    "key": None,
    "timestamp": None
}

# Limite máximo de acessos por usuário
max_access = 5

# Usuários permitidos e suas contagens de acesso
allowed_users = {
    "pstfr": 0,
    "emda": 0,
    "wndrsn": 0,
    "thglm": 0,
    "emrsnc": 0,
    "cslxnd": 0,
    "wlsn": 0,
    "edrd": 0,
    "vttb": 0,
    "tmmz": 0,
    "wltr": 0,
    "crtntt": 0,
    "wndrsn": 0,
    "rcrd": 0,
    "ndrtx": 0,
    "vttbt": 0,
    "mrn": 0,
    "rflcr": 0,
    "cnt": 0,
    "wbss": 0,
    "zr1": 0,
    "nbsbt": 0,
}  # Adicione os usuários permitidos aqui

# Função para gerar uma chave aleatória
def generate_key():
    return secrets.token_hex(16)  # Gera uma chave hexadecimal de 16 bytes

# Função para verificar se a chave ainda é válida
def is_key_valid():
    if key_data["key"] and key_data["timestamp"]:
        current_time = time.time()
        # Verifica se a chave ainda é válida (5 minutos = 300 segundos)
        if current_time - key_data["timestamp"] <= 300:
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        if username in allowed_users:  # Verifica se o usuário está na lista permitida
            if allowed_users[username] < max_access:  # Verifica se o usuário atingiu o limite de acessos
                if not is_key_valid():
                    key_data["key"] = generate_key()
                    key_data["timestamp"] = time.time()
                
                allowed_users[username] += 1  # Incrementa a contagem de acessos do usuário
                access_count = allowed_users[username]

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
                        .ad-banner {{
                            width: 728px;
                            height: 90px;
                            background-color: #f4f4f4;
                            padding: 10px;
                            text-align: center;
                            position: fixed;
                            bottom: 0;
                            box-shadow: 0 -2px 4px rgba(0,0,0,0.2);
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
                        <p>{key_data["key"]}</p>
                        <p>Acesso realizado: {access_count}/{max_access}</p>
                    </div>
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
        if data['key'] == key_data['key'] and is_key_valid():
            return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
