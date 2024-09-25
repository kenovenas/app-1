# Função para sincronizar os usuários permitidos sem resetar os acessos existentes
def sync_user_data(allowed_users_template):
    # Adicionar novos usuários permitidos sem alterar os existentes
    for user, data in allowed_users_template.items():
        if user not in user_access_history:
            # Se o usuário não está no histórico, adicionamos ele com as informações iniciais
            user_access_history[user] = {"visits": 0, "max_visits": data["max_visits"]}
        else:
            # Se o usuário já existe, garantimos que o número máximo de acessos é atualizado
            user_access_history[user]["max_visits"] = data["max_visits"]
    
    # Remover usuários do histórico que não estão mais na lista de permitidos
    for user in list(user_access_history.keys()):
        if user not in allowed_users_template:
            del user_access_history[user]

# Exemplo de como o código será executado ao adicionar ou remover usuários
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
    save_access_data(user_access_history)  # Salva o histórico sincronizado

    if request.method == 'POST':
        username = request.form.get('username')
        if username in user_access_history:
            user_data = user_access_history[username]

            # Verifica se o usuário já excedeu o número máximo de acessos
            if user_data["visits"] >= user_data["max_visits"]:
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
            user_data["visits"] += 1
            save_access_data(user_access_history)  # Salva a contagem de acessos

            # Gera uma nova chave se a anterior estiver expirada
            if "key_data" not in user_data or not is_key_valid(user_data["key_data"]):
                user_data["key_data"] = {
                    "key": generate_key(),
                    "timestamp": time.time()
                }
                save_access_data(user_access_history)  # Salva a chave gerada

            # Exibe a chave e as informações de acesso
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
                    .author {{
                        position: absolute;
                        top: 10px;
                        left: 10px;
                        color: #000;
                        font-size: 18px;
                    }}
                    .banner-telegram {{
                        position: absolute;
                        top: 10px;
                        right: 10px;
                        background-color: #0088cc;
                        padding: 10px;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    }}
                    .banner-telegram a {{
                        color: #ffcc00;
                        text-decoration: none;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="author">Autor = Keno Venas</div>
                <div class="banner-telegram">
                    <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Grupo do Telegram</a>
                </div>
                <div class="content">
                    <h1>Access Key</h1>
                    <p>Chave: {user_data["key_data"]["key"]}</p>
                    <p>Acessos Realizados: {user_data["visits"]} de {user_data["max_visits"]}</p>
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
        <style>
            .telegram-button {{
                background-color: #0088cc;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin-top: 20px;
                cursor: pointer;
            }}
            .telegram-button:hover {{
                background-color: #005f99;
            }}
        </style>
    </head>
    <body>
        <h1>Digite seu usuário</h1>
        <form method="POST">
            <input type="text" name="username" required>
            <button type="submit">Acessar</button>
        </form>
        <p>Entrar em contato para ter acesso:</p>
        <a href="https://t.me/Keno_venas" target="_blank" class="telegram-button">Keno Venas</a>
    </body>
    </html>
    '''
