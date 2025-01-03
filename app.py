from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Configura o logging
logging.basicConfig(level=logging.INFO)

# Lista de usuários autorizados
usuarios_autorizados = [
     "ok1390", "ok1203", "ok6675", "ok1999", "ok1820",
"ok5178", "ok1880", "ok1001", "ok0908", "ok1101", "ok9019",
      "ok3286", "ok9988", "ok2956", "ok1698", "ok3003",
    "ok1982", "ok9904", "ok1525", "ok2508", "ok0198",
    "ok1516", "ok1101", "ok0902", "admin", "bete", 
]

# Dicionário para rastrear visitas dos usuários
contador_visitas = {usuario: 0 for usuario in usuarios_autorizados}

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    usuario = data.get('usuario')

    if usuario in usuarios_autorizados:
        # Incrementa o contador de visitas
        contador_visitas[usuario] += 1
        visitas = contador_visitas[usuario]
        logging.info(f"Usuário autorizado: {usuario} - Visitas: {visitas}")  # Log do nome do usuário e contagem de visitas
        return jsonify({'autorizado': True, 'visitas': visitas}), 200
    else:
        logging.warning(f"Tentativa de acesso não autorizada: {usuario}")  # Log de acesso não autorizado
        return jsonify({'autorizado': False}), 403  # Forbidden

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
