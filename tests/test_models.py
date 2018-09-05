'''Test models.'''

from api.models import Meal, Order, User
from .base import BaseCase

class TestModels(BaseCase):
    '''Class for testing the user model.'''

    def test_user(self):
        '''Test user model.'''

        # Test saving a user.
        result = self.user1.save()
        expected = {
            'username': 'user1',
            'id': 1,
            'roles':[],
            'email': 'user1@email.com'}
        self.assertDictEqual(result, expected)

        # Test getting a user.
        self.assertIsInstance(User.get(id=1), User)

        # Test getting a user by key.
        self.assertIsInstance(User.get_by_key(username='user1'), User)

        # Test get all users.
        self.assertIsInstance(User.get_all(), dict)
        self.assertEqual(1, len(User.get_all()))

        # Test updating a user.
        new_data = {'username': 'New Username'}
        result = self.user1.update(new_data)
        self.assertEqual(result['username'], new_data['username'])

        # Test deleting a user.
        self.user1.delete()
        self.assertEqual(None, User.get(id=1))
        self.assertEqual(0, len(User.get_all()))
        self.assertEqual(None, User.get_by_key(username='user1'))

    def test_meal(self):
        '''Test meal model.'''

        # Test saving a meal.
        result = self.meal1.save()
        expected = {'price': 100.0, 'id': 1, 'name': 'Meal1'}
        self.assertDictEqual(result, expected)
        
        # Test getting a meal.
        self.assertIsInstance(Meal.get(id=1), Meal)

        # Test get all meals.
        self.assertIsInstance(Meal.get_all(), dict)
        self.assertEqual(1, len(Meal.get_all()))

        # Test updating a meal.
        new_data = {'name': 'New name'}
        result = self.meal1.update(new_data)
        self.assertEqual(result['name'], new_data['name'])

        # Test deleting a meal.
        self.meal1.delete()
        self.assertEqual(None, Meal.get(id=1))
        self.assertEqual(0, len(Meal.get_all()))

    def test_order(self):
        '''Test order model.'''

        # Test saving an order
        result = sorted(list(self.order1.save().keys()))
        expected = sorted(['id', 'total', 'user', 'time', 'meals'])
        self.assertEqual(result, expected)

        # Test getting a order.
        self.assertIsInstance(Order.get(id=1), Order)

        # Test get all orders.
        self.assertIsInstance(Order.get_all(), dict)
        self.assertEqual(1, len(Order.get_all()))

        # Test updating an order.
        new_data = {'user_id': 1, 'meals_dict': {1: 4}}
        result = self.order1.update(new_data)
        self.assertEqual(result['meals'][0]['quantity'], 4)

