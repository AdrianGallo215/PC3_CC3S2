import bcrypt
import jwt
import datetime

PRIVATEKEY = "AdGallo15122001"

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(username, password, database):

    if username in database:
        raise ValueError("Ya existe el nombre de usuario ingresado, por favor, elige otro.")
    else:
        try:
            database[username] = hash_password(password)
            return "Usuario registrado con éxito."
        except:
            raise ValueError("Error al registrar el usuario.")
        
def auth_user(username, password, database):
    if username not in database:
        raise ValueError("Nombre de usuario incorrecto.")

    if not check_password(database[username], password):
        raise ValueError("Contraseña incorrecta.")
    
    payload = {"username": username, "exp":datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)}
    token = jwt.encode(payload, PRIVATEKEY,algorithm="HS256")
    return token
  

def validate_token(token):
    try:
        decode = jwt.decode(token,PRIVATEKEY,algorithms=["HS256"])
        return decode
    except jwt.ExpiredSignatureError:
        raise ValueError("El token ha expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")