import pytest
from auth_service import JWTAuthService
from controller import UserController
from repository import InMemoryUserRepository
import datetime


class TestAuthService():

    def setup_method(self):
        self.auth_service = JWTAuthService()
        self.user_repository = InMemoryUserRepository()
        self.user_controller = UserController(self.auth_service,self.user_repository)

        self.user = self.user_controller.createUser('testing_user', 'Testing_password01', 'visitor')

    def teardown_method(self):
        self.user_repository.deleteUser(self.user)

    def test_valid_authenticate_user(self):
        token = self.auth_service.authenticate_user(self.user,'Testing_password01')

        assert token is not None

    def test_invalid_authenticate_user(self):
        with pytest.raises(ValueError, match="Contraseña incorrecta"):
            token = self.auth_service.authenticate_user(self.user,'Testing_password03')

    def test_generate_token(self):
        payload = {'id': self.user.id, 'username': self.user.username, 'role': self.user.role, 'permissions': self.user.permission, 'exp':datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)}
        
        token = self.auth_service.generate_token(payload)

        assert token is not None

    def test_valid_token(self): 
        payload = {'id': self.user.id, 'username': self.user.username, 'role': self.user.role, 'permissions': self.user.permission, 'exp':datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)}
        token = self.auth_service.generate_token(payload)
        
        data = self.auth_service.validate_token(token)
        
        assert data.get('username') == 'testing_user'
    
    def test_expired_token(self):
        payload = {'id': self.user.id, 'username': self.user.username, 'role': self.user.role, 'permissions': self.user.permission, 'exp':0}
        token = self.auth_service.generate_token(payload)

        with pytest.raises(ValueError, match="El token ha expirado"):
            self.auth_service.validate_token(token)

    def test_invalid_token(self):
        with pytest.raises(ValueError, match="Token inválido"):
            self.auth_service.validate_token('invalid.token')
    
    def test_no_token(self):
        with pytest.raises(ValueError, match="Necesitas ingresar un token"):
            self.auth_service.validate_token(None)

    def test_manipulated_token(self):
        payload = {'id': self.user.id, 'username': self.user.username, 'role': self.user.role, 'permissions': self.user.permission, 'exp':datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)}
        token = self.auth_service.generate_token(payload)
        newToken = str(token) + 'Hola'

        with pytest.raises(ValueError, match="Token inválido"):
            self.auth_service.validate_token(newToken)
