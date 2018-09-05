"""Base test class."""

from unittest import TestCase


from api.models import db, Meal, Order, User
from main import create_app


class BaseCase(TestCase):
    """Base class to be inherited by all other testcases."""

    def setUp(self):
        """Set up test application."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user1 = User(
            username='user1',
            email='user1@email.com',
            password='pass#123')
        self.user1.save()
    

    def tearDown(self):
        """Delete database and recreate it with no data."""
        self.app_context.pop()
