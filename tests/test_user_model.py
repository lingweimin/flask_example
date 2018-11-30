import unittest
from ..app.models.auth import User, Role
from app import create_app, db


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='123456')
        self.assertTrue(u.password_hash is not None)

    def test_password_verification(self):
        u = User(password='123456')
        self.assertTrue(u.verify_password('123456'))
