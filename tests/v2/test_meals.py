'''Tests meal resource.'''


from json import loads, dumps
from tests.v2.base import BaseCase

MEALS_URL = '/api/v2/meals/'
MEAL_URL = '/api/v2/meals/1'


class TestMealResource(BaseCase):
    '''Test the meal resources.'''

    def test_can_create_a_meal(self):
        '''Test the POST functionality for a meal.'''

        # Get admin token.
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        # Using valid data.
        response = self.client.post(
            MEALS_URL, data=self.valid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 201)
        expected = 'Meal successfully added.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        # Using duplicate meal.
        response = self.client.post(
            MEALS_URL, data=self.valid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 409)
        expected = 'Meal with that name already exists.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        #Using invalid name
        response = self.client.post(
            MEALS_URL, data={'name':"@lop",'price':600}, headers=headers)
        self.assertEqual(400,response.status_code)
        # Using invalid data.
        response = self.client.post(
            MEALS_URL, data=self.invalid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Name (str) is required.'
        self.assertEqual(
            loads(response.data.decode('utf-8'))['message']['name'], expected)
        # Provide a valid meal name and try it again.
        self.invalid_meal_data.update({'name': 'Meal 1'})
        response = self.client.post(
            MEALS_URL, data=self.invalid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Price (int) is required.'
        self.assertEqual(
            loads(response.data.decode('utf-8'))['message']['price'], expected)

    def test_only_admin_can_create_a_meal(self):
        # Test only an admin can create a meal.
        token = self.get_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            MEALS_URL, data=self.valid_meal_data2, headers=headers)
        self.assertEqual(response.status_code, 403)
        expected = 'This action requires an admin token.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_token_required_to_create_meal(self):
        # Test invalid headers.
        response = self.client.post(
            MEALS_URL, data=self.valid_meal_data,
            headers={})
        self.assertEqual(response.status_code, 400)
        expected = 'Ensure you have an authorization header.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_can_get_meals(self):
        '''Test GET functionality of meals.'''
        self.meal1.add_meal()
        # Test getting all meals.
        token = self.get_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.get(MEALS_URL, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(loads(response.data.decode('utf-8'))['meals'])

        # Test getting single meal.
        response = self.client.get(MEAL_URL, headers=headers)
        self.assertEqual(response.status_code, 200)
        expected = 'Meal found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertTrue(loads(response.data.decode('utf-8'))['meal'])

        # Test returns 404 for non-existent meal.
        response = self.client.get('/api/v2/meals/4', headers=headers)
        self.assertEqual(response.status_code, 404)
        expected = 'Meal not found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_can_edit_meal(self):
        '''Test editing of meals.'''
        self.meal1.add_meal()
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        #  edit meal
        response = self.client.put(
            MEAL_URL, data=dumps({'name': 'newmeal'}), headers=headers)
        # self.assertEqual(response.status_code, 200)
        expected = 'Meal has been updated successfully.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

        # invalid data
        response = self.client.put(
            MEAL_URL, data=dumps({'name': 12}), headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Invalid name!'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_only_admin_can_edit_meal(self):
        '''Test protection of meals.'''
        self.meal1.add_meal()
        token = self.get_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        #  edit meal
        response = self.client.put(
            MEAL_URL, data=dumps({'name': 'new meal'}), headers=headers)
        self.assertEqual(response.status_code, 403)
        expected = 'This action requires an admin token.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)


    def test_can_delete_meal(self):
        '''Test deletion of meals.'''
        self.meal1.add_meal()
        headers = {'Authorization': 'Bearer {}'.format(self.get_admin_token())}
        non_admin_headers = {
            'Authorization': 'Bearer {}'.format(self.get_user_token())}

        # Test non-admin cannot detete meal.
        response2 = self.client.delete(MEAL_URL, headers=non_admin_headers)
        self.assertEqual(
            loads(response2.data.decode('utf-8'))['message'],
            'This action requires an admin token.')
        response3 = self.client.delete(MEAL_URL, headers=headers)

        self.assertEqual(
            loads(response3.data.decode('utf-8'))['message'], 'Meal 1 successfully deleted.')

        response4 = self.client.get(MEALS_URL, headers=headers)
        self.assertEqual(loads(response4.data.decode('utf-8'))
                         ['message'], 'No meals found.')
        # Attempt deleting nonexistent meal.
        response5 = self.client.delete(
            '/api/v2/meals/10', headers=headers)
        self.assertEqual(
            loads(response5.data.decode('utf-8'))['message'], 'Meal does not exist')
