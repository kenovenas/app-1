from flask import Flask, render_template, request, redirect, session
import random
import string

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Lista de usuários permitidos
usuarios_permitidos = ['usuario1', 'usuario2']

# Função para gerar senha aleatória
def gerar_senha(tamanho=16):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    if username in usuarios_permitidos:
        session['username'] = username
        senha_gerada = gerar_senha()
        return render_template('key_page.html', senha=senha_gerada)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
