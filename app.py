from flask import Flask, request, render_template_string
import time
import json
import os

app = Flask(__name__)

# Dicionário global de histórico de acesso
user_access_history = {}

# Função para carregar dados de acesso de um arquivo JSON
def load_access_data():
    global user_access_history
    if os.path.exists('access_data.json'):
        with open('access_data.json', 'r') as f:
            user_access_history = json.load(f)

# Função para salvar dados de acesso em um arquivo JSON
def save_access_data(data):
    with open('access_data.json', 'w') as f:
        json.dump(data, f)

# Função para gerar uma chave de acesso
def generate_key():
    return str(int(time.time()))  # Exemplo simples de chave baseada em timestamp

# Função para validar a chave (exemplo com expiração de 5 minutos)
def is_key_valid(key_data):
    current_time = time.time()
    return current_time - key_data["timestamp"] <= 5 * 60  # 5 minutos de validade

# Função para sincronizar os usuários permitidos sem resetar os acessos existentes
def sync_user_data(allowed_users_template):
    for user, data in allowed_users_template.items():
        if user not in user_access_history:
            user_access_history[user] = {"visits": 0, "max_visits": data["max_visits"]}
        else:
            user_access_history[user]["max_visits"] = data["max_visits"]

    for user in list(user_access_history.keys()):
        if user not in allowed_users_template:
            del user_access_history[user]

# Carrega os dados de acesso ao iniciar o servidor
load_access_data()

# Exemplo de rota principal
@app.route('/', methods=['GET', 'POST'])
def home():
    # Template de usuários permitidos
    allowed_users_template = {
        "usuario1": {"max_visits": 10},
        "usuario2": {"max_visits": 5},
        "usuario_configurado": {"max_visits": 10}
    }

    # Sincroniza os dados dos usuários sem resetar os acessos
    sync_user_data(allowed_users_template)
    save_access_data(user_access_history)

    if request.method == 'POST':
        username = request.form.get('username')
        if username in user_access_history:
            user_data = user_access_history[username]

            if user_data["visits"] >= user_data["max_visits"]:
                return render_template_string('''
                    <h1>Acesso Negado</h1>
                    <p>Você atingiu o limite máximo de acessos.</p>
                ''')

            user_data["visits"] += 1
            save_access_data(user_access_history)

            if "key_data" not in user_data or not is_key_valid(user_data["key_data"]):
                user_data["key_data"] = {
                    "key": generate_key(),
                    "timestamp": time.time()
                }
                save_access_data(user_access_history)

            return render_template_string(f'''
            <h1>Access Key</h1>
            <p>Chave: {user_data["key_data"]["key"]}</p>
            <p>Acessos Realizados: {user_data["visits"]} de {user_data["max_visits"]}</p>
            ''')

        else:
            return "Acesso negado"

    return '''
    <h1>Digite seu usuário</h1>
    <form method="POST">
        <input type="text" name="username" required>
        <button type="submit">Acessar</button>
    </form>
    <p>Entrar em contato para ter acesso.</p>
    '''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
