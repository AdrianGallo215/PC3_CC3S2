import unittest
import pytest
from unittest.mock import Mock, MagicMock
from repository import InMemoryPostRepository, InMemoryUserRepository
from models import User, Post

class TestRepository(unittest.TestCase):

    def test_add_user(self):
        fake_repo = InMemoryUserRepository()
        user = User('test_user', 'test_password01')
        fake_repo.addUser(user)

        assert fake_repo.userList == {user.getId(), user}

    def test_update_user(self):
        fake_repo = InMemoryUserRepository()
        user = User('test_user', 'test_password01')
        fake_repo.addUser(user)
        user.username = 'test_user_2'

        fake_repo.updateUser(user)

        assert fake_repo.userList[user.getId()].username == 'test_user_2'

    def test_delete_user_valid(self):
         