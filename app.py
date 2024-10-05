from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import sqlite3
import secrets
import time

app = Flask(__name__)
CORS(app)

# Conectar ao banco de dados SQLite
def connect_db():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS keys
                      (id INTEGER PRIMARY KEY, key TEXT, timestamp REAL)''')
    conn.commit()
    return conn

# Função para gerar uma chave aleatória
def generate_key():
    return secrets.token_hex(16)  # Gera uma chave hexadecimal de 16 bytes

# Função para armazenar a chave no banco de dados
def store_key(key, timestamp):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO keys (key, timestamp) VALUES (?, ?)', (key, timestamp))
    conn.commit()
    conn.close()

# Função para recuperar a chave do banco de dados
def get_key():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT key, timestamp FROM keys ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result

# Função para verificar se a chave ainda é válida
def is_key_valid():
    key_data = get_key()
    if key_data:
        stored_key, stored_timestamp = key_data
        current_time = time.time()
        # Verifica se a chave ainda é válida (24 horas = 86400 segundos)
        if current_time - stored_timestamp <= 86400:
            return True, stored_key
    return False, None

# Lista de usuários permitidos
allowed_users = ["user1", "user2", "kenovenas"]

@app.route('/')
def login():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f9;
            }
            .login-container {
                text-align: center;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                background-color: white;
                width: 300px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .login-container h1 {
                margin-bottom: 20px;
            }
            .login-container form {
                display: flex;
                flex-direction: column;
                width: 100%;
            }
            .login-container input {
                padding: 10px;
                margin-bottom: 10px;
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .login-container button {
                padding: 10px 20px;
                background-color: #0088cc;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }
            .login-container button:hover {
                background-color: #005f99;
            }
            .contact {
                margin-top: 20px;
            }
            .author-link {
                color: #0088cc;
                text-decoration: none;
                font-weight: bold;
            }
            .telegram-group {
                margin-top: 10px;
            }
            .telegram-group a {
                color: #ffcc00;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>Login</h1>
            <form action="/login" method="post">
                <input type="text" id="username" name="username" placeholder="Usuário" required><br>
                <button type="submit">Login</button>
            </form>
            <div class="contact">
                <p>Para acessar entre em contato:</p>
                <a class="author-link" href="https://t.me/Keno_venas" target="_blank">Keno Venas</a>
            </div>
            <div class="telegram-group">
                <p>Grupo do Telegram:</p>
                <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Crypto Faucets</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['username']
    if username in allowed_users:
        return redirect(url_for('home', logged_in=True))
    else:
        return '''
        <h1>Usuário não autorizado!</h1>
        <a href="/">Voltar para o login</a>
        '''

@app.route('/home')
def home():
    logged_in = request.args.get('logged_in', None)
    if logged_in != 'True':
        return redirect(url_for('login'))

    valid, stored_key = is_key_valid()
    if not valid:
        new_key = generate_key()
        store_key(new_key, time.time())
        stored_key = new_key

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
        </style>
    </head>
    <body>
        <div class="author">Autor: Keno Venas</div>
        <div class="content">
            <h1>Access Key</h1>
            <p>{stored_key}</p>
        </div>
    </body>
    </html>
    '''

@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.get_json()
    valid, stored_key = is_key_valid()
    if 'key' in data and data['key'] == stored_key and valid:
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
