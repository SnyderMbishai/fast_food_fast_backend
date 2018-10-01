'''Test orders.'''
from json import dumps, loads
from tests.v2.base import BaseCase
from api.v2.models.user_model import User
from api.v2.models.order_model import Order

ORDERS_URL = '/api/v2/orders/'
ORDER_URL = '/api/v2/orders/1'
ACCEPT_URL = '/api/v2/orders/accept/1'


class TestOrderResource(BaseCase):
    '''Test order resources.'''

    def test_can_create_a_order(self):
        '''Test the POST functionality for an order.'''
        self.user1.add_user()
        self.meal1.add_meal()

        # Request data.
        valid_order_data = dumps({"user_id": 1, "meal_dict": {1: 3}})
        invalid_order_data = dumps({"user_id": "a", "meal_dict": {1: 3}})
        # Get user token to create header.
        token = self.user1.generate_token(id=1)
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
        self.meal1.add_meal()
        user_token = self.get_user_token()
        self.order1.add_order()

        user_header = {'Authorization': 'Bearer {}'.format(user_token)}

        # Add an extra user.
        self.user2 = User(
            username='user2', email='user2@email.com', password='pass#123')
        self.user2.add_user()
        self.order2 = Order(2, {1: 4})
        self.order2.add_order()

        token = self.get_admin_token()
        user2_header = {'Authorization': 'Bearer {}'.format(token)}

        # User request get one.
        response = self.client.get(ORDER_URL, headers=user2_header)
        self.assertEqual(response.status_code, 200)
        expected = 'Order found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertTrue(loads(response.data.decode('utf-8'))['order'])

        # User 1 cannnot see user 2's order.
        response = self.client.get('/api/v2/orders/2', headers=user_header)
        self.assertEqual(response.status_code, 403)
        expected = 'You do not have permission to see this order.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

        # Returns 404 if order does not exist.
        response = self.client.get('/api/v2/orders/4', headers=user_header)
        self.assertEqual(response.status_code, 404)
        expected = 'Order not found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)



    def test_user_can_only_get_their_order(self):
        self.user1.add_user()
        self.meal1.add_meal()
        self.order1.add_order()
        self.user2 = User(
            username='user2', email='user2@email.com', password='pass#123')
        self.user2.add_user()
        token = self.user2.generate_token(id=2)
        order = Order(2, {1: 4})
        order.add_order()

        user2_token = {'Authorization': 'Bearer {}'.format(
            token)}

        # User request get all.
        response = self.client.get(ORDERS_URL, headers=user2_token)

        self.assertEqual(response.status_code, 200)
        expected = 'Orders found.'
        orders = loads(response.data.decode('utf-8'))['orders']
        self.assertEqual(loads(response.data.decode('utf-8'))['message']
                         , expected)
        print(orders[0].keys())
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]['order_id'], 2)

    def test_admin_can_get_all_orders(self):
        self.meal1.add_meal()
        self.user1.add_user()
        self.order1.add_order()

        self.user2 = User(
            username='user2', email='user2@email.com', password='pass#123')
        self.user2.add_user()
        self.order2 = Order(2, {1: 4})
        self.order2.add_order()

        # Admin request.
        admin_token = self.get_admin_token()
        admin_header = {'Authorization': 'Bearer {}'.format(admin_token)}
        response = self.client.get(ORDERS_URL, headers=admin_header)
        self.assertEqual(response.status_code, 200)
        expected = 'Orders found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertEqual(
            len(loads(response.data.decode('utf-8'))['orders']), 2)

    def test_can_edit_order(self):
        '''Test PUT functionality of order.'''

        self.meal1.add_meal()
        user_token = self.get_user_token()
        user_header = {'Authorization': 'Bearer {}'.format(user_token)}
        self.order1.add_order()
        # New data.
        new_data = dumps({'new_data': {'meals_dict': {1: 4}}})
        response = self.client.put(
            ORDER_URL, data=new_data, headers=user_header)
        self.assertEqual(response.status_code, 200)
        result = loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Order updated successfully.')

        self.assertEqual(result['new_order']['meals'][0]['quantity'], 4)

    def test_admin_can_mark_order_as_completed(self):
        '''Test admin completing order.'''
        self.meal1.add_meal()
        self.user1.add_user()
        self.order1.add_order()
        admin_token = self.get_admin_token()
        headers = {"Authorization": "Bearer {}". format(admin_token)}
        # Admin can mark as completed.
        response = self.client.patch(ORDER_URL, headers=headers)
        self.assertEqual(response.status_code, 200)
        expected = 'Order 1 has been completed.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        # Mark a non-existent order.
        response = self.client.patch('/api/v2/orders/3', headers=headers)
        self.assertEqual(response.status_code, 404)
        expected = 'Order does not exist.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

        # Test cannot accept/decline an already completed oredr.
        response = self.client.patch(
            ACCEPT_URL, data=dumps({'accepted': False}), headers=headers)
        self.assertEqual(response.status_code, 200)
        expected = 'This order has already been completed.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_admin_can_decline_accept_order(self):
        '''Test admin declining order.'''
        self.meal1.add_meal()
        self.user1.add_user()
        self.order1.add_order()
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
            '/api/v2/orders/accept/3',
            data=dumps({'accepted': True}), headers=headers)
        self.assertEqual(response.status_code, 404)
        expected = 'Order does not exist.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

        # Test accepted is boolean.
        response = self.client.patch(
            ACCEPT_URL, data=dumps({'accepted': 'p'}), headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = 'accept should be a boolean.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
