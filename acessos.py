import json
import os

ACESSOS_FILE = 'acessos.json'

# Função para carregar acessos de um arquivo JSON
def load_accesses():
    if not os.path.exists(ACESSOS_FILE):
        return {}
    with open(ACESSOS_FILE, 'r') as f:
        return json.load(f)

# Função para salvar acessos em um arquivo JSON
def save_accesses(access_data):
    with open(ACESSOS_FILE, 'w') as f:
        json.dump(access_data, f, indent=4)

# Função para atualizar o acesso de um usuário
def update_access(username):
    access_data = load_accesses()  # Carrega os dados existentes
    user_access_count = access_data.get(username, 0)  # Obtém a contagem atual

    # Atualiza a contagem
    access_data[username] = user_access_count + 1
    save_accesses(access_data)  # Salva a nova contagem
