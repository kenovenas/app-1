import sqlite3

def add_user(username, max_visits):
    with sqlite3.connect('user_data.db') as conn:
        conn.execute('INSERT INTO users (username, max_visits) VALUES (?, ?)', (username, max_visits))
        conn.commit()

# Exemplo de adição de usuários
add_user('usuario1', 5)
add_user('usuario2', 3)
add_user('usuario3', 7)
