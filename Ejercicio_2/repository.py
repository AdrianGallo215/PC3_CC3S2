from abc import ABC, abstractmethod
from models import Post, User

class UserRepository(ABC):

    @abstractmethod
    def addUser(self, user: User):
        pass

    @abstractmethod
    def updateUser(self, user: User):
        pass

    @abstractmethod
    def getUserById(self, user_id):
        pass

    @abstractmethod
    def getUserByUsername(self, username):
        pass

    @abstractmethod
    def getAllUsers(self):
        pass

class PostRepository(ABC):
    @abstractmethod
    def addPost(self, post: Post):
        pass
    
    @abstractmethod
    def updatePost(self, post: Post):
        pass
    
    @abstractmethod
    def deletePost(self, post: Post):
        pass
    
    @abstractmethod
    def getPostById(self, postId):
        pass

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.userList = {}

    def addUser(self, user):
        self.userList[user.getId()] = user

    def updateUser(self, user):
        self.userList[user.getId()] = user

    def deleteUser(self, user):
        if int(user.getId()) not in self.userList:
            raise ValueError("User no encontrado.")
        del self.userList[user.getId()]

    def getUserById(self, user_id):
        return self.userList.get(user_id, None)
    
    def getUserByUsername(self, username):
        return next((u for u in self.userList.values() if u.username == username), None)
    
    def getAllUsers(self):
        return self.userList.values()
    
class InMemoryPostRepository(PostRepository):
    def __init__(self):
        self.postList = {}

    def addPost(self, post):
        self.postList[post.getId()] = post

    def updatePost(self, post):
        if int(post.getId()) not in self.postList:
            raise ValueError("Post no encontrado.")
        self.postList[post.getId()] = post

    def deletePost(self, post):
        if int(post.getId()) not in self.postList:
            raise ValueError("Post no encontrado.")
        del self.postList[post.getId()]

    def getPostById(self, postId):
        return self.postList.get(postId, None)