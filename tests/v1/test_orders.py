'''Test orders.'''
from json import dumps, loads
from tests.v1.base import BaseCase
from api.v1.models import User, Order

ORDERS_URL = '/api/v1/orders/'
ORDER_URL = '/api/v1/orders/1'
ACCEPT_URL = '/api/v1/orders/accept/1'


class TestOrderResource(BaseCase):
    '''Test order resources.'''

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
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])
        # Check order create with invalid user_id.
        response = self.client.post(
            ORDERS_URL, data=invalid_order_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'user_id (int) is required.'
        # Check correct message returned.
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])
        # Check order create with invalid meal_dict.
        invalid_order_data = dumps({"user_id": 1, 'meal_dict': []})
        response = self.client.post(
            ORDERS_URL, data=invalid_order_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'meal_dict (dict) is required.'
        # Check correct message returned.
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])
        # Create order for non-existent meal.
        valid_order_data = dumps({'user_id': 2, 'meal_dict': {2: 3}})
        response = self.client.post(
            ORDERS_URL, data=valid_order_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Meal 2 does not exist.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])
        # Place order with invalid quantity.
        valid_order_data = dumps({'user_id': 2, 'meal_dict': {1: 'b'}})
        response = self.client.post(
            ORDERS_URL, data=valid_order_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Meal quantities should be integers.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])
        # Place order with invalid meal_id.
        valid_order_data = dumps({'user_id': 2, 'meal_dict': {'a': 1}})
        response = self.client.post(
            ORDERS_URL, data=valid_order_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Meal ID should be an integer.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])

    def test_can_get_order(self):
        '''Test users can access their orders but admin can see all orders.'''

        user_token = self.get_user_token()
        admin_token = self.get_admin_token()
        user_header = {'Authorization': 'Bearer {}'.format(user_token)}
        admin_header = {'Authorization': 'Bearer {}'.format(admin_token)}
        # Add an extra user.
        self.user2 = User(
            username='user2', email='user2@email.com', password='pass#123')
        self.user2.save()
        self.order2 = Order(2, {1: 4})
        self.order2.save()
        # User request get one.
        response = self.client.get(ORDER_URL, headers=user_header)
        self.assertEqual(response.status_code, 200)
        expected = 'Order found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertTrue(loads(response.data.decode('utf-8'))['order'])
        # User request get all.
        response = self.client.get(ORDERS_URL, headers=user_header)
        self.assertEqual(response.status_code, 200)
        expected = 'Orders found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertEqual(
            len(loads(response.data.decode('utf-8'))['orders']), 1)
        # Admin request.
        response = self.client.get(ORDERS_URL, headers=admin_header)
        self.assertEqual(response.status_code, 200)
        expected = 'Orders found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertEqual(
            len(loads(response.data.decode('utf-8'))['orders']), 2)
        # User 1 cannnot see user 2's order.
        response = self.client.get('/api/v1/orders/2', headers=user_header)
        self.assertEqual(response.status_code, 403)
        expected = 'You do not have permission to see this order.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        # Returns 404 if order does not exist.
        response = self.client.get('/api/v1/orders/4', headers=user_header)
        self.assertEqual(response.status_code, 404)
        expected = 'Order not found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_can_edit_order(self):
        '''Test PUT functionality of order.'''

        user_token = self.get_user_token()
        user_header = {'Authorization': 'Bearer {}'.format(user_token)}
        # Add an extra user.
        self.user2 = User(
            username='user2', email='user2@email.com', password='pass#123')
        self.user2.save()
        # Order for new user.
        self.order2 = Order(2, {1: 4})
        self.order2.save()
        # New data.
        new_data = dumps({'new_data': {'meals_dict': {1: 4}}})
        response = self.client.put(
            ORDER_URL, data=new_data, headers=user_header)
        self.assertEqual(response.status_code, 200)
        result = loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Order updated successfully.')

    def test_admin_can_mark_order_as_completed(self):
        '''Test admin completing order.'''

        admin_token = self.get_admin_token()
        headers = {"Authorization": "Bearer {}". format(admin_token)}
        # Admin can mark as completed.
        response = self.client.patch(ORDER_URL, headers=headers)
        self.assertEqual(response.status_code, 200)
        expected = 'Order 1 has been completed.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        # Mark a non-existent order.
        response = self.client.patch('/api/v1/orders/3', headers=headers)
        self.assertEqual(response.status_code, 404)
        expected = 'Order does not exist.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_admin_can_decline_accept_order(self):
        '''Test admin declining order.'''

        admin_token = self.get_admin_token()
        headers = {"Authorization": "Bearer {}". format(admin_token)}
        # Test can accept
        response = self.client.patch(
            ACCEPT_URL, data=dumps({'accepted': True}), headers=headers)
        self.assertEqual(response.status_code, 200)
        expected = 'Order 1 has been accepted.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        # Test can decline.
        response = self.client.patch(
            ACCEPT_URL, data=dumps({'accepted': False}), headers=headers)
        self.assertEqual(response.status_code, 200)
        expected = 'Order 1 has been declined.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        # Test cannot accept/decline non existent.
        response = self.client.patch(
            '/api/v1/orders/accept/3',
            data=dumps({'accepted': True}), headers=headers)
        self.assertEqual(response.status_code, 404)
        expected = 'Order does not exist.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.order1.completed = True
        self.order1.save()
        # Test cannot edit an already completed oredr.
        response = self.client.patch(
            ACCEPT_URL, data=dumps({'accepted': False}), headers=headers)
        self.assertEqual(response.status_code, 200)
        expected = 'This order has already been completed.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        # Test accepted is boolean.
        response = self.client.patch(
            ACCEPT_URL, data=dumps({'accepted': 'p'}), headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = 'accept should be a boolean.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
