from flask import Flask, request, jsonify, render_template_string
import sqlite3
import secrets
import time
import os

app = Flask(__name__)
application = app

# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect('user_data.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                max_visits INTEGER NOT NULL,
                visits INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

# Inicializar o banco de dados ao iniciar o aplicativo
init_db()

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
    if request.method == 'POST':
        username = request.form.get('username')
        
        with sqlite3.connect('user_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user_data = cursor.fetchone()
            
            if user_data:  # Verifica se o usuário existe no banco de dados
                visits = user_data[3]  # Obtém a contagem de acessos
                max_visits = user_data[2]  # Obtém o máximo de acessos

                # Verifica se o usuário já excedeu o número máximo de acessos
                if visits >= max_visits:
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
                cursor.execute('UPDATE users SET visits = visits + 1 WHERE username = ?', (username,))
                conn.commit()

                key_data = {
                    "key": generate_key(),
                    "timestamp": time.time()
                }
                
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
                    </style>
                </head>
                <body>
                    <div class="content">
                        <h1>Access Key</h1>
                        <p>{key_data["key"]}</p>
                        <p>Você já acessou {visits + 1} de {max_visits} vezes.</p>
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
        if data['key'] == key_data['key'] and is_key_valid(key_data):
            return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
