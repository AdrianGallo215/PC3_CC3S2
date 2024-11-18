from abc import ABC, abstractmethod 
import jwt
import datetime
from hash import check_password, PRIVATEKEY
from models import User

class AuthService(ABC):

    @abstractmethod
    def authenticate_user(self, user, password):
        pass

    @abstractmethod
    def generate_token(self, payload):
        pass

    @abstractmethod
    def validate_token(self, token):
        pass

class JWTAuthService(AuthService):

    def authenticate_user(self, user: User, password):
        if not check_password(user.password, password):
            raise ValueError("Contraseña incorrecta")
        
        payload = {'id': user.id, 'username': user.username, 'role': user.role, 'permissions': user.permission, 'exp':datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)}
        return self.generate_token(payload)    
    
    def generate_token(self, payload):
        token = jwt.encode(payload, PRIVATEKEY, algorithm='HS256')
        return token
    
    def validate_token(self, token):
        if token:
            try:
                return jwt.decode(token,PRIVATEKEY,algorithms=["HS256"])                
            except jwt.ExpiredSignatureError:
                raise ValueError("El token ha expirado")
            except jwt.InvalidTokenError:
                raise ValueError("Token inválido")
        raise ValueError("Necesitas ingresar un token")
            