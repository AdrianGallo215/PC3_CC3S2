import unittest
import pytest
from unittest.mock import Mock, MagicMock
from repository import InMemoryPostRepository, InMemoryUserRepository
from models import User, Post

class TestUserRepository(unittest.TestCase):

    def test_add_user(self):
        fake_repo = InMemoryUserRepository()
        user = User('test_user', 'test_password01')
        fake_repo.addUser(user)

        assert fake_repo.userList.get(user.getId()) == user

    def test_update_user(self):
        fake_repo = InMemoryUserRepository()
        user = User('test_user', 'test_password01')
        fake_repo.addUser(user)
        user.username = 'test_user_2'

        fake_repo.updateUser(user)

        assert fake_repo.userList[user.getId()].username == 'test_user_2'

    def test_delete_user_valid(self):
        fake_repo = InMemoryUserRepository()
        user = User('test_user', 'test_password01')
        fake_repo.addUser(user)

        fake_repo.deleteUser(user)

        assert fake_repo.getUserById(user.getId()) == None

    def test_delete_user_invalid(self):
        fake_repo = InMemoryUserRepository()
        user = User('test_user', 'test_password01')

        with pytest.raises(ValueError,match="User no encontrado."):
            fake_repo.deleteUser(user)
    
    def test_get_user_by_id(self):
        mock_repo = Mock()
        mock_user = User('test_user', 'test_password01')
        mock_repo.getUserById.return_value = mock_user

        user = mock_repo.getUserById(1)

        assert user.username == 'test_user'
        assert user.role == 'visitor'

    
    def test_get_user_by_id_invalid(self):
        fake_repo = InMemoryUserRepository()

        user = fake_repo.getUserById(2)

        assert user is None

    def test_get_user_by_username(self):
        mock_repo = Mock()
        mock_user = User('test_user', 'test_password01')
        mock_repo.getUserByUsername.return_value = mock_user

        user = mock_repo.getUserByUsername('test_user')

        assert user.username == 'test_user'
        assert user.role == 'visitor'

    def test_get_user_by_username_invalid(self):
        fake_repo = InMemoryUserRepository()

        user = fake_repo.getUserByUsername('test_user_2')

        assert user is None

    def test_get_all_users(self):
        fake_repo = InMemoryUserRepository()
        user1 = User('test_user', 'test_password01')
        user2 = User ('test_user2', 'test_password01')
        fake_repo.addUser(user1)
        fake_repo.addUser(user2)
        
        users = fake_repo.getAllUsers()
        
        assert list(users)[0].username == 'test_user'
        assert list(users)[1].role == 'visitor'
        assert len(list(users)) == 2

    def test_get_all_users_empty(self):
        fake_repo = InMemoryUserRepository()
        users = fake_repo.getAllUsers()
        assert len(list(users)) == 0

class TestPostRepository(unittest.TestCase):

    def setUp(self):
        self.fake_post_repo = InMemoryPostRepository()
        self.post = Post('test_post', 'test_author','This is a test')
        self.fake_post_repo.addPost(self.post)
    
    def tearDown(self):
        self.fake_post_repo.postList.clear()

    def test_add_post(self):
        assert self.fake_post_repo.postList.get(self.post.getId()) == self.post

    def test_update_post(self):        
        self.post.title = 'test_post_2'

        self.fake_post_repo.updatePost(self.post)

        assert self.fake_post_repo.postList[self.post.getId()].title == 'test_post_2'

    def test_delete_post_valid(self):
        self.fake_post_repo.deletePost(self.post)

        assert self.fake_post_repo.getPostById(self.post.getId()) == None

    def test_delete_post_invalid(self):
        post2 = Post('new_test_post', 'new_test_author', 'new_Test_content')
        with pytest.raises(ValueError,match="Post no encontrado."):
            self.fake_post_repo.deletePost(post2)
    
    def test_get_post_by_id(self):
        mock_repo = Mock()
        mock_post = Post('mock_test_post', 'mock_author', 'mock content')
        mock_repo.getPostById.return_value = mock_post

        post = mock_repo.getPostById(1)

        assert post.title == 'mock_test_post'
        assert post.author == 'mock_author'

    
    def test_get_post_by_id_invalid(self):

        post = self.fake_post_repo.getPostById(2)

        assert post is None
 