from models import User, Post
from auth import check_password, hash_password,PRIVATEKEY, validate_user_data
import datetime
import jwt
class UserController():

    def __init__(self):
        self.userList = {}
        self.postController = PostController()

    def createUser(self, username, password, role):
        validate_user_data(username, password, role)

        if any(user.username == username for user in self.userList.values()):
            raise ValueError("Este nombre de usuario ya se encuentra registrado")

        user = User(username, hash_password(password), role)

        self.userList[user.getId()] = user
        return user.getData()
    
    def getUserById(self, id, database):
        try:
            return database.get(id)
        except:
            raise ValueError("No se encontró ningún usuario con ese id")
    
    def authUser(self, username, password):
        user = next((u for u in self.userList.values() if u.username == username), None)
    
        if not user:
            raise ValueError("Usuario no encontrado")
        if not check_password(user.password, password):
            raise ValueError("Contraseña incorrecta")
        
        payload = {'username':username, 'id': user.getId(), 'role':user.role, 'permissions':user.permission, "exp":datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)}
        token = jwt.encode(payload, PRIVATEKEY,algorithm='HS256')
        return token

    def change_password(self, user_id, new_password, old_password):
        user = self.userList.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        if not check_password(user.password, old_password):
            raise ValueError("Contraseña actual incorrecta")
        user.password = hash_password(new_password)
        self.userList[user_id] = user
        return "Contraseña cambiada exitosamente"
    
    def getUsers(self):
        userdata={}
        for user in self.userList.values():
            userdata[user.getId()] = user.getData()

        return userdata

class PostController():

    def __init__(self):
        self.listPosts = {}

    def createPost(self, title, author, content):
        post  = Post(title, author, content)
        self.listPosts[post.getId()] = post
        return {post.getId():post.getData()}

    def getPostById(self, id):
        post = self.listPosts.get(int(id))
        if not post:
            raise ValueError("No se encontró ningún post con ese ID.")
        return post
        

    def readPost(self, post_id):
        post=self.getPostById(post_id)
        return post.read()
    
    def editPost(self, post_id, content):
        post = self.getPostById(post_id)
        return post.write(content)
    
    def deletePost(self, post_id):
        if int(post_id) not in self.listPosts:
            raise ValueError("Post no encontrado.")
        del self.listPosts[int(post_id)]
        
    