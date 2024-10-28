from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Configura o logging
logging.basicConfig(level=logging.INFO)

# Lista de usuários autorizados
usuarios_autorizados = [
    "ok6675",
                 "ok3286",
                 "ok1390",
                 "zr1",
                 "mro",
                 "mrclm",
                 "mxwll",
                 "nmmr",
                        "mts",
                        "jncmps",
                        "dnln",
                       "ok1698",
                        "ok0091",
                        "ok0908",
                        "ok2508",
                        "ok2956",
                        "ok1203",
                        "ok9019",
                        "ok4004",
                        "ok1999",
                        "ok1982",
                         "ok0198",
    "ok1001",
    "ok2090",
    "ok0902",
    "admin"
]

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    usuario = data.get('usuario')

    if usuario in usuarios_autorizados:
        logging.info(f"Usuário autorizado: {usuario}")  # Log do nome do usuário
        return jsonify({'autorizado': True}), 200
    else:
        logging.warning(f"Tentativa de acesso não autorizada: {usuario}")  # Log de acesso não autorizado
        return jsonify({'autorizado': False}), 403  # Forbidden

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
