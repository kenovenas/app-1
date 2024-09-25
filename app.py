from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para utilizar sessões

# Lista simples de usuários permitidos (pode ser personalizada ou ampliada)
usuarios_permitidos = ["usuario1", "usuario2", "usuario3"]

# Função para gerar uma senha aleatória de 16 caracteres
def gerar_senha():
    caracteres = string.ascii_letters + string.digits
    senha = ''.join(random.choice(caracteres) for i in range(16))
    return senha

@app.route('/')
def home():
    return redirect(url_for('login'))

# Rota da página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        # Valida o nome de usuário
        if username in usuarios_permitidos:
            session['username'] = username  # Armazena o nome do usuário na sessão
            return redirect(url_for('acesso_key'))

        return "Acesso negado! Usuário não encontrado."

    return render_template('login.html')

# Rota para gerar e exibir a senha
@app.route('/acesso_key')
def acesso_key():
    if 'username' not in session:
        return redirect(url_for('login'))

    senha_aleatoria = gerar_senha()
    return render_template('key.html', senha=senha_aleatoria)

# Rota para logout (opcional)
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove o usuário da sessão
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
