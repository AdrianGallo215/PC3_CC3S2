import pytest
import re
from controller import UserController, PostController
from repository import InMemoryPostRepository, InMemoryUserRepository
from auth_service import JWTAuthService

class TestUserController():

    def setup_method(self):
        self.user_repository = InMemoryUserRepository()
        self.auth_Service = JWTAuthService()
        self.user_controller = UserController(self.auth_Service, self.user_repository)
        self.user = self.user_controller.createUser("test_user","test_password01","visitor")

    def teardown_method(self):
        self.user_repository.deleteUser(self.user)

    def test_invalid_username(self):
        with pytest.raises(ValueError, match=r"El nombre de usuario debe ser de al menos 3 caracteres."):
            self.user_controller.validate_user_data('a','Adrian_01', 'visitor')
        
    def test_no_username(self):
        with pytest.raises(ValueError, match=r"El nombre de usuario debe ser de al menos 3 caracteres."):
            self.user_controller.validate_user_data(None,'Adrian_01', 'visitor')

    def test_short_password(self):
        with pytest.raises(ValueError, match=r"La contraseña debe ser de al menos 8 caracteres."):
            self.user_controller.validate_user_data("Adrian",'a', 'visitor')

    def test_no_password(self):
        with pytest.raises(ValueError, match=r"La contraseña debe ser de al menos 8 caracteres."):
            self.user_controller.validate_user_data("Adrian",None, 'visitor')

    def test_no_numbers_in_password(self):
        with pytest.raises(ValueError, match=r"La contraseña debe tener al menos 1 número"):
            self.user_controller.validate_user_data("Adrian",'Adrianadrian', 'visitor')

    def test_no_special_characters_in_password(self):
        with pytest.raises(ValueError, match=re.escape('La contraseña debe tene algún caracter especial (".", "_", "@", "!")')):
            self.user_controller.validate_user_data("Adrian",'Adrianadrian01', 'visitor')

    def test_invalid_role(self):
        with pytest.raises(ValueError, match=r'El rol no es válido'):
            self.user_controller.validate_user_data("Adrian",'Adrian_01', 'aaa')

    def test_no_role(self):
        with pytest.raises(ValueError, match=r'El rol no es válido'):
            self.user_controller.validate_user_data("Adrian",'Adrian_01', None)

    def test_valid_user_data(self):
        try:
            self.user_controller.validate_user_data("Adrian",'Adrian_01', 'visitor')
        except ValueError:
            pytest.fail("validate_user_data lanzó ValueError con datos válidos")

    def test_create_user_valid(self):
        user = self.user_controller.createUser("Adrian","Adrian_01","visitor")

        assert user.username == "Adrian"
        assert user.role == "visitor"
        assert user.password is not None

    def test_create_user_invalid(self):
        with pytest.raises(ValueError, match="Este nombre de usuario ya se encuentra registrado"):
            self.user_controller.createUser("test_user", "Adrian_01","visitor")

    def test_change_password_valid(self):
        user_id  = self.user.getId()
        
        res = self.user_controller.change_password(user_id, "test_password02", "test_password01")

        assert res == "Contraseña cambiada exitosamente"

    def test_wrong_user_change_password(self):
        with pytest.raises(ValueError,match="Usuario no encontrado"):
            res = self.user_controller.change_password(1000, "test_password02", "test_password01")

    def test_wrong_password_change_password(self):
        with pytest.raises(ValueError, match="Contraseña actual incorrecta"):
            user_id = self.user.getId()
            res = self.user_controller.change_password(user_id, "test_password02", "Adrian_01")

    def test_valid_authUser(self):
        token = self.user_controller.authUser("test_user","test_password01")
        decoded = self.auth_Service.validate_token(token)

        assert token is not None
        assert decoded.get("username") == "test_user"
        assert decoded.get("role") == "visitor"

    def test_invalid_authUser(self):
        with pytest.raises(ValueError, match="Nombre de usuario incorrecto."):
            self.user_controller.authUser("Holaaaa", "Adrian_01")

class TestPostController():

    def setup_method(self):
        self.post_repository = InMemoryPostRepository()
        self.post_controller = PostController(self.post_repository)
        self.sample_post = self.post_controller.createPost("Título de prueba", "Autor", "Contenido inicial")

    def teardown_method(self):
        self.post_repository.postList.clear()

    def test_create_post_valid(self):
        post = self.post_controller.createPost("Nuevo título", "Nuevo autor", "Nuevo contenido")
        
        assert post.title == "Nuevo título"
        assert post.author == "Nuevo autor"
        assert post.content == "Nuevo contenido"

    def test_read_post_valid(self):
        post_id = self.sample_post.getId()
        content = self.post_controller.readPost(post_id)

        assert content == "Contenido inicial"

    def test_read_post_invalid(self):
        with pytest.raises(ValueError, match="Post no encontrado."):
            self.post_controller.readPost(999)

    def test_edit_post_valid(self):
        post_id = self.sample_post.getId()
        updated_content = "Contenido actualizado"
        
        new_content = self.post_controller.editPost(post_id, updated_content)

        assert new_content == updated_content

    def test_edit_post_invalid(self):
        with pytest.raises(ValueError, match="Post no encontrado."):
            self.post_controller.editPost(999, "Intento de contenido")