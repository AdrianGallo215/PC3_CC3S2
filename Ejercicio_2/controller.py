from models import User
class UserController():

    def __init__(self):
        pass

    def getUserById(self, id, database):
        for user, data in database.items:
            if data.get('id') == id:
                return User(user, data.get('password'), data.get('role'), data.get('permissions'))
        raise ValueError("No se encontró ningún usuario con ese id")