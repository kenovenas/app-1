import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Configuração de logging para garantir que as mensagens apareçam no console do Render
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Lista de usuários autorizados
usuarios_autorizados = [
    "fiel", "ok6675", "crtntt", "ok3286", "ok1390", "zr1", "nbsbt", "mxchk",
    "pdrrm", "mro", "hmd", "mrclm", "mxwll", "nmmr", "mts", "jncmps", "dnln",
    "ok1698", "ok0091", "ok0908", "ok2508", "ok2956", "ok1203"
]

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    usuario = data.get('usuario')

    # Verifica se o usuário é autorizado
    if usuario in usuarios_autorizados:
        # Usa logging para registrar o usuário autorizado e o horário da requisição
        logging.info(f"Usuário autorizado: {usuario}")
        return jsonify({'autorizado': True}), 200
    else:
        # Usa logging para registrar a tentativa de acesso não autorizada
        logging.warning(f"Tentativa de acesso negada para o usuário: {usuario}")
        return jsonify({'autorizado': False}), 403  # Forbidden

if __name__ == '__main__':
    # Configura a porta para leitura dinâmica, conforme exigido pelo Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
