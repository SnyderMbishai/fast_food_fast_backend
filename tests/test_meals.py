'''Tests meal resource'''

from json import loads
from .base import BaseCase

MEALS_URL = '/api/v1/meals'
MEAL_URL = '/api/v1/meals/1'

class TestMealResource(BaseCase):
    '''Class for testing meals' views.'''

    def test_can_create_a_meal(self):
        '''Test can create a meal can be created.'''

        # Get admin token.
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}

        # Test can create using valid data.
        response = self.client.post(MEALS_URL, data=self.valid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 201)
        expected = {'message': 'Meal successfully added.'}
        self.assertEqual(loads(response.data)['message'], expected['message'])

        # Test creating a duplicate meal.
        response = self.client.post(MEALS_URL, data=self.valid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 202)
        expected = {'message': 'Meal with that name already exists.'}
        self.assertEqual(loads(response.data)['message'], expected['message'])

        # Test creating using invalid data.
        response = self.client.post(MEALS_URL, data=self.invalid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = {'message': 'Name (str) is required.'}
        self.assertEqual(loads(response.data)['message']['name'], expected['message'])

        # Test using a valid meal name and try it again.
        self.invalid_meal_data.update({'name': 'Meal 1'})
        response = self.client.post(MEALS_URL, data=self.invalid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = {'message': 'Price (int) is required.'}
        self.assertEqual(loads(response.data)['message']['price'], expected['message'])

    def test_only_admin_can_crate_meal(self):
        '''Test that an admin only can perform certain tasks.'''

        # Get user token.
        token = self.get_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}

        # Create a meal using as a user.
        response = self.client.post(MEALS_URL, data=self.valid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 403)
        expected = {'message': 'You do not have permission to perform this action'}
        self.assertEqual(loads(response.data)['message'], expected['message'])