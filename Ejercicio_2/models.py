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

