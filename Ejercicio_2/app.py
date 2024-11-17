from flask import Flask, request, jsonify
from auth import auth_user, validate_token, register_user, change_password
app = Flask(__name__)

database = {'adrian': {'id': 1, 'password': b'$2b$12$nli8RUuFvqdiy.CkCowGsuuiJ5S8xVvBkN1XUQVuzMb10lk7jbkJC', 'role': 'editor', 'permissions': ['read', 'edit']}}

@app.route('/')
def home():
    return "Flask works!"

@app.route('/signup', methods=['POST'])
def signUp():
    data = request.json

    try:
        res = register_user(data.get('username'), data.get('password'), database, role = "editor")
        return jsonify({"res":res}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

@app.route('/login', methods=['POST'])
def logIn():
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    try:
        token = auth_user(username, password, database)
        return jsonify({"token":token}), 200
    except ValueError as e:
        return jsonify({"Error":str(e)}), 401

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token requerido"}), 401
    
    try:
        decoded = validate_token(token)
        return jsonify({"greetings": f"Bienvenido, {decoded['username']}"}), 200
    except ValueError as e:
        return jsonify({"error": "Token inválido"}), 401
    
@app.route('/changepassword', methods=['POST'])
def changePassword():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token requerido"}), 401
    
    data = request.json

    try:
        res = change_password(token, data.get('newpassword'), data.get('oldpassword'), database)
        return jsonify({"res":res}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    

if __name__ == '__main__':
    app.run(debug=True)