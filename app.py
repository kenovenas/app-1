from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import secrets
import time

app = Flask(__name__)
CORS(app)
app.secret_key = 'supersecretkey'  # Chave secreta para sessões

# Armazenamento para chave e seu timestamp
key_data = {
    "key": None,
    "timestamp": None
}

# Lista de usuários permitidos
allowed_users = ["user1", "user2", "kenovenas"]

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

# Rota para a página de login
@app.route('/')
def login():
    if 'user' in session:
        return redirect(url_for('home'))  # Redireciona para a página principal se já estiver logado
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                flex-direction: column;
            }}
            .content {{
                text-align: center;
            }}
            .author-link {{
                color: #0088cc;
                text-decoration: none;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="content">
            <h1>Login</h1>
            <form action="/login" method="post">
                <label for="username">Usuário:</label><br>
                <input type="text" id="username" name="username" required><br><br>
                <button type="submit">Login</button>
            </form>
            <p>Para acessar entre em contato:</p>
            <a class="author-link" href="https://t.me/Keno_venas" target="_blank">Keno Venas</a>
        </div>
    </body>
    </html>
    '''

# Rota de autenticação
@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['username']
    if username in allowed_users:
        session['user'] = username
        return redirect(url_for('home'))
    return '''
    <h1>Usuário não autorizado!</h1>
    <a href="/">Voltar para o login</a>
    '''

# Rota para a página principal que exibe a chave após login
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    if not is_key_valid():
        key_data["key"] = generate_key()
        key_data["timestamp"] = time.time()

    return f'''
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
        </div>

        <!-- Script da Hydro -->
        <script id="hydro_config" type="text/javascript">
            window.Hydro_tagId = "ab51bfd4-d078-4c04-a17b-ccfcfe865175";
        </script>
        <script id="hydro_script" src="https://track.hydro.online/"></script>

        <!-- anuncios -->
        <div class="ad-banner">
            <script type="text/javascript">
                atOptions = {{
                    'key' : '78713e6d4e36d5a549e9864674183de6',
                    'format' : 'iframe',
                    'height' : 90,
                    'width' : 728,
                    'params' : {{}}
                }};
            </script>
            <script type="text/javascript" src="//spiceoptimistic.com/78713e6d4e36d5a549e9864674183de6/invoke.js"></script>
        </div>
        <script type='text/javascript' src='//spiceoptimistic.com/1c/66/88/1c668878f3f644b95a54de17911c2ff5.js'></script>
    </body>
    </html>
    '''

# Rota para fazer logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/validate', methods=['POST'])
def validate_key():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if 'key' in data:
        if data['key'] == key_data['key'] and is_key_valid():
            return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
