"""Test the welcome view funciton."""
from json import loads

from tests.base import BaseCase


class TestWelcome(BaseCase):
    """Welcome resource tests."""

    def test_welcome(self):
        """Test welcome endpoint."""
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        expected = {'message': 'Welcome to Fast Food Fast.'}
        self.assertEqual(expected, loads(response.data))
        