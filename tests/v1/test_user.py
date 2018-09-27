"""Test the user view funciton."""
from json import loads, dumps

from tests.v1.base import BaseCase


class TestUser(BaseCase):
    """User resource tests."""

    def test_create_user(self):
        """Test create  user endpoint."""

        # test correct signup
        response = self.client.post(
            '/api/v1/users/signup', data=self.user_data_1)
        self.assertEqual(201, response.status_code)
        expected = {'message': 'User registration successful'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
        self.assertTrue(loads(response.data.decode('utf-8'))['token'])

        # test duplicate signup
        response = self.client.post(
            '/api/v1/users/signup', data=self.user_data_1)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Username already taken, if you are registered,please login to continue.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])

        # test signup using invalid username
        response = self.client.post(
            '/api/v1/users/signup', data=self.user_data_2)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Invalid username.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])

        # test signup using inavalid email
        response = self.client.post(
            '/api/v1/users/signup', data=self.user_data_3)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Invalid email.Example of a valid one:hero@gmail.com'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])

        # test signup using inavalid password
        self.user_data_3.update(
            {'username': 'user3', 'email': 'user3@mail.com', 'password': '', 'confirm_password': ''})
        response = self.client.post(
            '/api/v1/users/signup', data=self.user_data_3)
        self.assertEqual(400, response.status_code)
        expected = {
            'message': 'Invalid password. Password should be 8 or more characters long.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
