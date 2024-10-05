from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lista de usuários permitidos
allowed_users = ["user1", "user2", "kenovenas"]

# Rota para a página de login
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
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>Login</h1>
            <form id="loginForm" onsubmit="return false;">
                <input type="text" id="username" name="username" placeholder="Usuário" required><br>
                <button id="loginButton">Login</button>
            </form>
            <div class="contact">
                <p>Para acessar entre em contato:</p>
                <a class="author-link" href="https://t.me/Keno_venas" target="_blank">Keno Venas</a>
            </div>
        </div>
        <script>
            document.getElementById('loginButton').addEventListener('click', function() {
                const username = document.getElementById('username').value;

                fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username: username }),
                })
                .then(response => {
                    if (response.ok) {
                        // Usuário autenticado
                        alert("Usuário autenticado com sucesso!");
                        // Aqui você pode redirecionar ou chamar a função principal
                    } else {
                        // Usuário não autenticado
                        alert("Usuário não autorizado!");
                    }
                })
                .catch(error => console.error('Erro:', error));
            });
        </script>
    </body>
    </html>
    '''

# Rota para autenticação
@app.route('/login', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    if username in allowed_users:
        return jsonify({"authenticated": True}), 200
    else:
        return jsonify({"authenticated": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
