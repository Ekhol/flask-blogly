from app import app
from models import User, Post, PostTag, Tag
from unittest import TestCase


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        with self.client:
            result = self.client.get('/')
            self.assertIn(b'Recent Posts', result.data)

    def test_users(self):
        with self.client:
            result = self.client.get('/users')
            self.assertIn(b'Users', result.data)
