'''Test orders.'''
from json import dumps, loads
from .base import BaseCase
from api.models import User, Order

ORDERS_URL = '/api/v1/orders/'
ORDER_URL = '/api/v1/orders/1'
ACCEPT_URL = '/api/v1/orders/accept/1'


class TestOrderResource(BaseCase):
    '''Test the meal resources.'''

    def test_can_create_a_order(self):
        '''Test the POST functionality for an order.'''

        # Request data.
        valid_order_data = dumps({"user_id": 1, "meal_dict": {1: 3}})
        invalid_order_data = dumps({"user_id": "a", "meal_dict": {1: 3}})
        
        # Get user token to create header.
        token = self.get_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        
        # Using valid data.
        response = self.client.post(
            ORDERS_URL, data=valid_order_data, headers=headers)        
        # Check status code is 201
        self.assertEqual(response.status_code, 201)
        expected = 'Order has been created successfully.'        
        # Check correct message returned.
        self.assertEqual(expected, loads(response.data)['message'])
        
        # Check order create with invalid user_id.
        response = self.client.post(
            ORDERS_URL, data=invalid_order_data, headers=headers)        
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'user_id (int) is required.'        
        # Check correct message returned.
        self.assertEqual(expected, loads(response.data)['message'])
        
        # Check order create with invalid meal_dict.
        invalid_order_data = dumps({"user_id": 1, 'meal_dict': []})
        response = self.client.post(
            ORDERS_URL, data=invalid_order_data, headers=headers)        
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'meal_dict (dict) is required.'        
        # Check correct message returned.
        self.assertEqual(expected, loads(response.data)['message'])
        
        # Create order for non-existent meal.
        valid_order_data = dumps({'user_id': 2, 'meal_dict': {2: 3}})
        response = self.client.post(
            ORDERS_URL, data=valid_order_data, headers=headers)        
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Meal 2 does not exist.'
        self.assertEqual(expected, loads(response.data)['message'])
        
        # Place order with invalid quantity.
        valid_order_data = dumps({'user_id': 2, 'meal_dict': {1: 'b'}})
        response = self.client.post(
            ORDERS_URL, data=valid_order_data, headers=headers)        
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Meal quantities should be integers.'
        self.assertEqual(expected, loads(response.data)['message'])
        
        # Place order with invalid meal_id.
        valid_order_data = dumps({'user_id': 2, 'meal_dict': {'a': 1}})
        response = self.client.post(
            ORDERS_URL, data=valid_order_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Meal ID should be an integer.'
        self.assertEqual(expected, loads(response.data)['message'])