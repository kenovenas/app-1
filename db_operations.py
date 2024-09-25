import sqlite3

# Função para inicializar o banco de dados e criar a tabela se não existir
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS allowed_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Função para adicionar usuários permitidos ao banco de dados
def add_initial_users():
    users = ["pstfr", "emda", "wndrsn"]  # Adicione aqui os nomes de usuário desejados
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    for username in users:
        cursor.execute('INSERT OR IGNORE INTO allowed_users (username) VALUES (?)', (username,))
    conn.commit()
    conn.close()

# Função para adicionar um único usuário
def add_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO allowed_users (username) VALUES (?)', (username,))
    conn.commit()
    conn.close()

# Função para obter a lista de usuários permitidos
def get_allowed_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM allowed_users')
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users
