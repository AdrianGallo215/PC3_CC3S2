import bcrypt
import jwt
import datetime
from models import User

PRIVATEKEY = "AdGallo15122001"

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
        
def validate_user_data(username, password, role):
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

def change_password(data, newpassword, oldpassword, database):
    username = data.get("username")

    if username not in database:
        raise ValueError("Usuario no encontrado en la base de datos")
    
    if not check_password(database[username]['password'], oldpassword):
            raise ValueError("La contraseña actual es incorrecta.")
    try:
        database[username]['password'] = hash_password(newpassword)
        return("La contraseña fue cambiada exitosamente")
    except Exception as e:
        raise ValueError(f"La contraseña no se pudo cambiar: {str(e)}")

def validate_token(token):
    if token:
        try:
            decode = jwt.decode(token,PRIVATEKEY,algorithms=["HS256"])
            return decode
        except jwt.ExpiredSignatureError:
            raise ValueError("El token ha expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido")
    raise ValueError("Necesitas ingresar un token")