import pytest
from auth_service import JWTAuthService
from controller import UserController
from repository import InMemoryUserRepository

auth_service = JWTAuthService()
user_repository = InMemoryUserRepository()
user_controller = UserController(auth_service,user_repository)

class TestAuthService():

    def setup_method(self):
        self.user = user_controller.createUser('testing_user', 'Testing_password01', 'visitor')

    def teardown_method(self):
        user_repository.deleteUser(self.user)

    def test_valid_authenticate_user(self):
        token = auth_service.authenticate_user(self.user,'Testing_password01')

        assert token is not None

    def test_invalid_authenticate_user(self):
        token = auth_service.authenticate_user(self.user,'Testing_password03')

        assert token is None