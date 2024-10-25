import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuração detalhada do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Lista de usuários autorizados
usuarios_autorizados = [
    "fiel", "ok6675", "crtntt", "ok3286", "ok1390", "zr1", "nbsbt", "mxchk",
    "pdrrm", "mro", "hmd", "mrclm", "mxwll", "nmmr", "mts", "jncmps", "dnln",
    "ok1698", "ok0091", "ok0908", "ok2508", "ok2956", "ok1203"
]

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    logging.info("Recebida uma nova requisição no endpoint '/validar_usuario'")

    data = request.get_json()

    if not data:
        logging.warning("Nenhum dado JSON recebido na requisição.")
        return jsonify({'erro': 'Nenhum dado JSON enviado.'}), 400

    usuario = data.get('usuario')
    
    if usuario:
        logging.info(f"Nome do usuário recebido: {usuario}")
    else:
        logging.warning("Nenhum usuário fornecido na requisição.")
        return jsonify({'erro': 'Campo de usuário ausente.'}), 400

    if usuario in usuarios_autorizados:
        logging.info(f"Usuário autorizado: {usuario}")
        return jsonify({'autorizado': True}), 200
    else:
        logging.warning(f"Tentativa de acesso negada para o usuário: {usuario}")
        return jsonify({'autorizado': False}), 403

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
