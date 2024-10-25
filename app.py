from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Lista de usuários autorizados (substitua por um banco de dados em produção)
usuarios_autorizados = ["fiel",
                "ok6675",
                 "ok3286",
                 "ok1390",
                 "zr1",
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
                        "ok2508",
                        "ok2956",
                        "ok1203",
                        "ok9019",
                        "ok4004",
                        "ok1999",
                        "ok1982",
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
