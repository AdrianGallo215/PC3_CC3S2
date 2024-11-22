import unittest
import datetime
from models import User, Post

class TestUserModel(unittest.TestCase):

    def setUp(self):
        User.userCount = 0

    def test_create_user_with_default_role(self):
        user = User("test_user", "test_password")
        
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.password, "test_password")
        self.assertEqual(user.role, "visitor")
        self.assertEqual(user.permission, ["read"])
        self.assertEqual(user.id, 1)

    def test_create_user_with_editor_role(self):
        user = User("editor_user", "editor_password", "editor")
        
        self.assertEqual(user.role, "editor")
        self.assertEqual(user.permission, ["read", "edit"])

    def test_create_user_with_admin_role(self):
        user = User("admin_user", "admin_password", "admin")
        
        self.assertEqual(user.role, "admin")
        self.assertEqual(user.permission, ["read", "write", "delete"])

    def test_create_user_with_invalid_role(self):
        user = User("invalid_user", "invalid_password", "invalid_role")
        
        self.assertEqual(user.role, "visitor")
        self.assertEqual(user.permission, ["read"])

    def test_user_id_increments_correctly(self):
        user1 = User("user1", "password1")
        user2 = User("user2", "password2")
        
        self.assertEqual(user1.getId(), 1)
        self.assertEqual(user2.getId(), 2)

    def test_get_data(self):
        user = User("data_user", "data_password", "admin")
        data = user.getData()
        
        self.assertEqual(data['username'], "data_user")
        self.assertEqual(data['role'], "admin")
        self.assertEqual(data['permissions'], ["read", "write", "delete"])

    def test_invalid_role_raises_value_error(self):
        with self.assertRaises(ValueError, msg="Rol no definido"):
            User.roles.append("invalid_role") 
            User("user", "password", "invalid_role")
            User.roles.pop()  

class TestPostModel(unittest.TestCase):

    def setUp(self):
        Post.postCounter = 0 

    def test_create_post(self):
        post = Post("Test Title", "Test Author", "This is a test content")
        
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.author, "Test Author")
        self.assertEqual(post.content, "This is a test content")
        self.assertEqual(post.id, 1)
        self.assertIsInstance(post.creation_date, datetime.datetime)

    def test_post_id_increments_correctly(self):
        post1 = Post("Post 1", "Author 1", "Content 1")
        post2 = Post("Post 2", "Author 2", "Content 2")
        
        self.assertEqual(post1.getId(), 1)
        self.assertEqual(post2.getId(), 2)

    def test_read_post_content(self):
        post = Post("Read Test", "Test Author", "Test Content")
        content = post.read()
        
        self.assertEqual(content, "Test Content")

    def test_write_post_content(self):
        post = Post("Write Test", "Test Author", "Old Content")
        updated_content = post.write("Updated Content")
        
        self.assertEqual(updated_content, "Updated Content")
        self.assertEqual(post.content, "Updated Content")

    def test_get_data(self):
        post = Post("Data Test", "Test Author", "Test Content")
        data = post.getData()
        
        self.assertEqual(data['title'], "Data Test")
        self.assertEqual(data['author'], "Test Author")
        self.assertEqual(data['content'], "Test Content")
        self.assertEqual(data['id:'], 1)

if __name__ == '__main__':
    unittest.main()
