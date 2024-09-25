from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Lista de usuários permitidos
usuarios_permitidos = {'usuario1', 'usuario2'}  # Adicione os usuários permitidos aqui
acessos_realizados = set()  # Para registrar usuários que já acessaram

def gerar_senha():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        if usuario in usuarios_permitidos and usuario not in acessos_realizados:
            session['usuario'] = usuario
            acessos_realizados.add(usuario)
            return redirect(url_for('key'))
        return 'Usuário inválido ou já acessado.'

    return render_template('login.html')

@app.route('/key')
def key():
    if 'usuario' in session:
        senha = gerar_senha()
        return render_template('key.html', senha=senha)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
