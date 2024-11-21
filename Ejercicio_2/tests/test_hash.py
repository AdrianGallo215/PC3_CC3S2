import pytest
from hash import hash_password, check_password

class TestHash():

    def test_hash_password_valid(self):
        password = 'test_password01'
        hashed = hash_password(password)

        assert hashed != password.encode('utf-8')
        assert isinstance(hashed, bytes)

    def test_check_password_valid(self):
        password = 'test_password01'
        hashed = hash_password(password)

        assert check_password(hashed,password)

    def test_check_password_invalid(self):
        password = 'test_password01'
        hashed = hash_password(password)

        assert check_password(hashed, 'test_password_02') is False    

    def test_hash_password_unique(self):
        password1 = 'test_password01'
        password2 = 'test_password02'

        hashed1 = hash_password(password1)
        hashed2 = hash_password(password2)

        assert hashed1 != hashed2