import datetime
class User():

    userCount = 0
    roles = ["visitor", "editor", "admin"]
    permissions = ["read", "write", "delete"]

    def __init__(self, username, password, role = "visitor"):
        self.id = User.increaseUserCount()
        self.username = username
        self.password = password
        self.role = role if role in User.roles else "visitor"
        self.permission = []
        self.setPermissions()
        

    @classmethod
    def increaseUserCount(cls):
        cls.userCount += 1
        return cls.userCount
    
    def setPermissions(self):
        if(self.role == "visitor"):
            self.permission = ["read"]
        elif(self.role == "editor"):
            self.permission = ["read", "edit"]
        elif(self.role == "admin"):
            self.permission = ["read", "write", "delete"]
        else:
            raise ValueError("Rol no definido")
        
    def getId(self):
        return self.id
    
    def getData(self):
        return {'id': self.id, 'username': self.username, 'password': str(self.password), 'role': self.role, 'permissions':self.permission}

class Post():

    postCounter = 0

    def __init__(self, title, author, content):
        self.id = Post.increaseCounter()
        self.title = title
        self.author  = author
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        self.content = content

    @classmethod
    def increaseCounter(cls):
        cls.postCounter += 1
        return cls.postCounter
    
    def read(self):
        return self.content

    def write(self, content):
        self.content = content
        return self.content
    
    def getId(self):
        return self.id
    
    def getData(self):
        return {'id:': self.getId(), 'author': self.author, 'title': self.title ,'creation_date': self.creation_date, 'content': self.content}