'''Tests meal resource'''

from json import loads
from .base import BaseCase

MEALS_URL = '/api/v1/meals'
MEAL_URL = '/api/v1/meals/1'

class TestMealResource(BaseCase):
    '''Class for testing meals' views.'''

    def test_can_create_a_meal(self):
        '''Test can create a meal can be created.'''

        # Get admin token
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}

        # Test can create using valid data
        response = self.client.post(MEALS_URL, data=self.valid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 201)
        expected = {'message': 'Meal successfully added.'}
        self.assertEqual(loads(response.data)['message'], expected['message'])