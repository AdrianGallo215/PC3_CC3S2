from repository import UserRepository, PostRepository
from models import User, Post
from hash import check_password, hash_password
from auth_service import AuthService
class UserController():

    def __init__(self, authService:AuthService, userRepository: UserRepository):
        self.userRepository = userRepository
        self.authService = authService

    def validate_user_data(self, username, password, role):
        if not username or len(username) < 3:
            raise ValueError("El nombre de usuario debe ser de al menos 3 caracteres.")
        if not password or len(password) < 8:
            raise ValueError("La contraseña debe ser de al menos 8 caracteres.")
        if not any(char.isdigit() for char in password):
            raise ValueError("La contraseña debe tener al menos 1 número")
        if not any(char in [".", "_", "@", "!"] for char in password):
            raise ValueError('La contraseña debe tene algún caracter especial (".", "_", "@", "!")')
        if not role or role not in ["visitor", "editor", "admin"]:
            raise ValueError("El rol no es válido")

    def createUser(self, username, password, role):
        self.validate_user_data(username, password, role)

        if self.userRepository.getUserByUsername(username):
            raise ValueError("Este nombre de usuario ya se encuentra registrado")

        user = User(username, hash_password(password), role) 
        self.userRepository.addUser(user)

        return user

    def change_password(self, user_id, new_password, old_password):
        user = self.userRepository.getUserById(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        if not check_password(user.password, old_password):
            raise ValueError("Contraseña actual incorrecta")
        
        user.password = hash_password(new_password) 
        self.userRepository.updateUser(user)
        return "Contraseña cambiada exitosamente"
    
    def authUser(self, username, password):
        user = self.userRepository.getUserByUsername(username)
        if not user:
            raise ValueError("Nombre de usuario incorrecto.")
        return self.authService.authenticate_user(user, password)
    

class PostController():

    def __init__(self, postRepository: PostRepository):
        self.postRepository = postRepository

    def createPost(self, title, author, content):
        post  = Post(title, author, content)
        self.postRepository.addPost(post)
        return post

    def readPost(self, post_id):
        post=self.postRepository.getPostById(post_id)
        return post.read()
    
    def editPost(self, post_id, content):
        post = self.postRepository.getPostById(post_id)
        if not post:
            raise ValueError("Post no encontrado.")
        post.write(content)
        self.postRepository.updatePost(post)
        return post.read()
    