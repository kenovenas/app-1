from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir CORS

# Lista de usuários autorizados
usuarios_autorizados = {"pstfr", 
                 "emda",
                 "wndrsn",
                "thglm",
                "emrsnc",
                "cslxnd",
                "wlsn",
                "edrd",
                "vttb",
                "tmmz",
                "wltr",
                 "crtntt",
                 "wndrsn",
                 "rcrd",
                 "ndrtx",
                 "vttbt",
                 "mrn",
                 "rflcr",
                 "cnt",
                 "wbss",
                 "zr1",
                 "nbsbt",
                 "mxchk",
                 "pdrrm",
                 "kauan",
                 "mro",
                 "hmd",
                 "mrclm",
                 "mxwll",
                }  # Adicione seus usuários aqui

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    print("Dados recebidos:", data)  # Para depuração
    usuario = data.get('usuario')

    if usuario in usuarios_autorizados:
        return jsonify({"autorizado": True}), 200
    else:
        return jsonify({"autorizado": False}), 200

if __name__ == '__main__':
    app.run(debug=True)
