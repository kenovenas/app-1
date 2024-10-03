from flask import Flask, request, jsonify, render_template_string
import secrets
import time

app = Flask(__name__)

# Armazenamento para chave, timestamp e usuário
key_data = {
    "key": None,
    "timestamp": None,
    "user": None
}

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

# Página de login e exibição da chave
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = request.form.get('username')
        if user:
            # Armazenar o nome do usuário e gerar uma nova chave
            key_data["user"] = user
            key_data["key"] = generate_key()
            key_data["timestamp"] = time.time()

    user_logged_in = key_data["user"] is not None

    return render_template_string('''
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
                flex-direction: column;
                font-family: Arial, sans-serif;
            }}
            .content {{
                text-align: center;
            }}
            .author {{
                position: absolute;
                bottom: 10px;
                color: #000;
                font-size: 16px;
            }}
            a {{
                color: #0088cc;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="content">
            {% if not user_logged_in %}
                <h1>Login</h1>
                <form method="POST">
                    <label for="username">Usuário:</label><br>
                    <input type="text" id="username" name="username" required><br><br>
                    <button type="submit">Confirmar</button>
                </form>
                <p>Para ter acesso, entre em contato com <a href="https://t.me/Keno_venas" target="_blank">Keno Venas</a></p>
            {% else %}
                <h1>Bem-vindo, {{ key_data['user'] }}</h1>
                <p>Sua chave de acesso é:</p>
                <p><strong>{{ key_data['key'] }}</strong></p>
            {% endif %}
        </div>
        <div class="author">
            <p>Autor: <a href="https://t.me/Keno_venas" target="_blank">Keno Venas</a></p>
        </div>
    </body>
    </html>
    ''', user_logged_in=user_logged_in, key_data=key_data)

if __name__ == '__main__':
    app.run(debug=True)
