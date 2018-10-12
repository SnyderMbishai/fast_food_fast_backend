"""Base test class."""
from unittest import TestCase


from main import create_app


class BaseCase(TestCase):
    """Base class to be inherited by all other testcases."""

    def setUp(self):
        """Set up test application."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    

    def tearDown(self):
        """Delete database and recreate it with no data."""
        self.app_context.pop()
