from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Lista de usuários autorizados (substitua por um banco de dados em produção)
usuarios_autorizados = ["fiel",
                "tmmz",
                "ok6675",
                 "crtntt",
                 "wndrsn",
                 "rcrd",
                 "ndrtx",
                 "ok3286",
                 "mrn",
                 "rflcr",
                 "cnt",
                 "wbss",
                 "zr1",
                 "nbsbt",
                 "mxchk",
                 "pdrrm",
                 "mro",
                 "hmd",
                 "mrclm",
                 "mxwll",
                 "nmmr",
                        "mts",
                        "jncmps",
                        "dnln",
                       "ok1698",
                        "ok0091",
                        "ok0908",
                        "vttbt",
                       ]

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    usuario = data.get('usuario')

    if usuario in usuarios_autorizados:
        return jsonify({'autorizado': True}), 200
    else:
        return jsonify({'autorizado': False}), 403  # Forbidden

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
