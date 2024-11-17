import bcrypt
import jwt
import datetime
from models import User
from controller import UserController

PRIVATEKEY = "AdGallo15122001"

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(username, password, database, role = "visitor"):

    if username in database:
        raise ValueError("Ya existe el nombre de usuario ingresado, por favor, elige otro.")
    else:
        try:
            user = User(username, hash_password(password), role)
            database[username] = {
                'id': user.id,
                'password': user.password,
                'role': user.role,
                'permissions': user.permission
            }
            return "Usuario registrado con éxito."
        except KeyError:
            raise ValueError("Error al registrar el usuario.")
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")
        
def auth_user(username, password, database):
    if username not in database:
        raise ValueError("Nombre de usuario incorrecto.")

    if not check_password(database[username]['password'], password):
        raise ValueError("Contraseña incorrecta.")
    
    payload = {"username": username, "id":database[username]["id"], "role": database[username]["role"], "permissions": database[username]["permissions"], "exp":datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)}
    token = jwt.encode(payload, PRIVATEKEY,algorithm="HS256")
    return token

def change_password(token, newpassword, oldpassword, database):
    decode = validate_token(token)
    username = decode.get("username")

    if username not in database:
        raise ValueError("Usuario no encontrado en la base de datos")
    
    if not check_password(database[username]['password'], oldpassword):
            raise ValueError("La contraseña actual es incorrecta.")
    try:
        database[decode.get("username")]['password'] = hash_password(newpassword)
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