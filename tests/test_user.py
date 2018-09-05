"""Test the user view funciton."""
from json import loads, dumps

from tests.base import BaseCase


class TestUser(BaseCase):
    """User resource tests."""

    def test_create_user(self):
        """Test create  user endpoint."""

        # test correct signup
        response = self.client.post('/api/v1/users/signup', data=self.user_data_1)
        self.assertEqual(201, response.status_code)
        expected = {'message': 'User registration successful'}
        self.assertEqual(expected['message'], loads(response.data)['message'])
        self.assertTrue(loads(response.data)['token'])

        # test duplicate signup
        response = self.client.post('/api/v1/users/signup', data=self.user_data_1)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Username/Email not available.'}
        self.assertEqual(expected['message'], loads(response.data)['message'])

        # test signup using invalid username
        response = self.client.post('/api/v1/users/signup', data=self.user_data_2)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Invalid username.'}
        self.assertEqual(expected['message'], loads(response.data)['message'])