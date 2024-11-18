from flask import Flask, request, jsonify
from repository import InMemoryUserRepository, InMemoryPostRepository
from auth_service import JWTAuthService
from controller import PostController, UserController
from functools import wraps
app = Flask(__name__)

user_repository = InMemoryUserRepository()
post_repository = InMemoryPostRepository()
JWT = JWTAuthService()
usercontroller = UserController(JWT, user_repository)
postcontroller = PostController(post_repository)

def requerir_token(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        token = request.headers.get('Authorization')
         
        if not token:
            return jsonify({"error": "Token requerido"}), 401
        try:
            decoded = JWT.validate_token(token)
            return func(*args, **kwargs, user_data=decoded)
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
    return envoltorio

@app.route('/')
def home():
    return "Flask works!"

@app.route('/signup', methods=['POST'])
def signUp():
    data = request.json

    try:
        role = data.get('role', 'visitor')

        user = usercontroller.createUser(data.get('username'), data.get('password'), role)
        return jsonify({"res": user}), 200
    except ValueError as e: 
        return jsonify({'error': str(e)}), 401

@app.route('/login', methods=['POST'])
def logIn():
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    try:
        token = usercontroller.authUser(username, password)
        return jsonify({"token":token}), 200
    except ValueError as e:
        return jsonify({"Error":str(e)}), 401

@app.route('/protected', methods=['GET'])
@requerir_token
def protected(user_data):
    return jsonify({"greetings": f"Bienvenido, {user_data['username']}"}), 200
    

@app.route('/changepassword', methods=['POST'])
@requerir_token
def changePassword(user_data):
    data = request.json

    try:
        res = usercontroller.change_password(user_data['id'], data.get('newpassword'), data.get('oldpassword'))
        return jsonify({"res":res}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
@app.route('/create', methods=['POST'])
@requerir_token
def createPost(user_data):
    data = request.json

    title = data.get('title')
    content = data.get('content')

    try:
        post = postcontroller.createPost(title, user_data.get('username'),content)
        return jsonify({post.getId():post.getData()}), 200
    except ValueError as e:
        return jsonify({'error':str(e)}), 401
    
@app.route('/edit/<post_id>', methods = ['POST'])
@requerir_token
def edit_post(post_id, user_data):
    if user_data.get('role') not in ['editor','admin']:
        return jsonify({"error": "No tienes permisos de editor."}), 401
    
    data = request.json

    try:
        post = post_repository.getPostById(post_id)

        if user_data.get('role') == 'editor':
            if post.author != user_data.get('username'):
                return jsonify({"error": "No tienes permisos para editar archivos ajenos."}), 401
            
        newPost = postcontroller.editPost(post_id, data.get('content'))
        return jsonify(newPost), 200
        
    except ValueError as e:
        return jsonify({'error':str(e)}), 401
    
@app.route('/delete/<post_id>', methods=['POST'])
@requerir_token
def delete_post(post_id, user_data):
    if user_data.get('role') != 'admin':
        return jsonify({"error": "No tienes permisos de administrador."}), 401
    else:
        try:
            post_repository.deletePost(post_repository.getPostById(int(post_id)))
            return jsonify({"Success":f"Post con id {post_id} fue eliminado exitosamente"}), 200
        except ValueError as e:
            return jsonify({"Error": str(e)}), 401

    
@app.route('/getAllUsers')
def getAllUsers():
    return jsonify(usercontroller.getUsers()), 200
    

if __name__ == '__main__':
    app.run(debug=True)