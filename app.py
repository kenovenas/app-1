from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lista de usuários permitidos
allowed_users = ["user1", "user2", "kenovenas"]

@app.route('/login', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    if username in allowed_users:
        return jsonify({"authenticated": True}), 200
    return jsonify({"authenticated": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
