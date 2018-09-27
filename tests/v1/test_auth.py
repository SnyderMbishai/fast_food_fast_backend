"""Test the user view funciton."""
from json import loads, dumps

from tests.v1.base import BaseCase


class TestAuth(BaseCase):
    """User resource tests."""

    def test_auth_user(self):
        """Test create  user endpoint."""

        # test correct signin
        response = self.client.post(
            '/api/v1/users/signin',
            data={'username': 'user1', 'password': 'pass#123'})
        self.assertEqual(200, response.status_code)
        expected = {'message': 'User login successful.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
        self.assertTrue(loads(response.data.decode('utf-8'))['token'])

        # test signin with wrong password
        response = self.client.post(
            '/api/v1/users/signin',
            data={'username': 'user1', 'password': 'pass#1234'})
        self.assertEqual(401, response.status_code)
        expected = {'message': 'Wrong password.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])

        # test signin with nonexistent username
        response = self.client.post(
            '/api/v1/users/signin',
            data={'username': 'user2', 'password': 'pass#1234'})
        self.assertEqual(401, response.status_code)
        expected = {'message': 'Username not registered. Correct it or register first.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
