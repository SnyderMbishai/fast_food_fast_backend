'''Tests meal resource.'''


from json import loads, dumps
from tests.base import BaseCase

MEALS_URL = '/api/v1/meals/'
MEAL_URL = '/api/v1/meals/1'


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
        # Test only an admin can create a meal."""
        token = self.get_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            MEALS_URL, data=self.valid_meal_data, headers=headers)
        self.assertEqual(response.status_code, 403)
        expected = 'This action requires an admin token.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
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
        response = self.client.get('/api/v1/meals/4', headers=headers)
        self.assertEqual(response.status_code, 404)
        expected = 'Meal not found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_can_edit_meal(self):
        '''Test editing of meals.'''

        #get token
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        # create meal to edit
        response1 = self.client.post(
            MEALS_URL, data=self.valid_meal_data, headers=headers)
        self.assertEqual(response1.status_code, 201)
        #edit meal
      
    def test_only_admin_can_edit_meal(self):
        '''Test protection of meals.'''

        pass

    def test_can_delete_meal(self):
        '''Test deletion of meals.'''

        headers = {'Authorization': 'Bearer {}'.format(self.get_admin_token())}
        non_admin_headers = {
            'Authorization': 'Bearer {}'.format(self.get_user_token())}
        self.meal1.delete()  # Remove extra meal.
        # Create meal.
        res=self.client.post(
            MEALS_URL, data=self.valid_meal_data, headers=headers)
        print(res)
        response1 = self.client.get(MEALS_URL, headers=headers)
        # Confirm meal creation.
        self.assertTrue(loads(response1.data.decode('utf-8'))['meals'])
        # Test non-admin cannot detete meal.
        response2 = self.client.delete(MEAL_URL, headers=non_admin_headers)
        self.assertEqual(
            loads(response2.data.decode('utf-8'))['message'],
            'This action requires an admin token.')
        response3 = self.client.delete(MEAL_URL, headers=headers)
        response4 = self.client.get(MEALS_URL, headers=headers)
        self.assertEqual(
            loads(response3.data.decode('utf-8'))['message'], 'Meal 1 successfully deleted.')

        self.assertEqual(loads(response4.data.decode('utf-8'))
                         ['message'], 'No meals found.')
        # Attempt deleting nonexistent meal.
        response5 = self.client.delete(
            '/api/v1/meals/10', headers=headers)
        self.assertEqual(
            loads(response5.data.decode('utf-8'))['message'], 'Meal does not exist')
