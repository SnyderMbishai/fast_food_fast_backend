'''Test models.'''

from api.v2.models.meal_model import Meal
from api.v2.models.user_model import User
from api.v2.models.order_model import Order
from tests.v2.base import BaseCase


class TestModels(BaseCase):
    '''Class for testing the user model.'''

    def test_user(self):
        '''Test user model.'''

        # Test saving a user.
        self.user1.add_user()
        self.assertEqual(1, len(User.get_all()))

        # Test getting a user.
        self.assertIsInstance(User.get(id=1), tuple)

        # test default role assigned is user
        self.assertEqual(User.get_roles(user_id=1)[0], 'user')
        # Test getting a user by key.
        self.assertIsInstance(User.get(username='user1'), tuple)

        # Test get all users.
        self.assertIsInstance(User.get_all(), list)
        self.assertEqual(1, len(User.get_all()))

        # Test deleting a user.
        self.user1.delete_user(1)
        self.assertEqual(None, User.get(id=1))
        self.assertEqual(0, len(User.get_all()))
        self.assertEqual(None, User.get(username='user1'))

    def test_meal(self):
        '''Test meal model.'''
        pass
        self.assertEqual(0, len(Meal.get_all()))

        # # Test saving a meal.
        self.meal1.add_meal()
        self.assertEqual(1, len(Meal.get_all()))

        # Test getting a meal.
        self.assertIsInstance(Meal.get(id=1), tuple)

        # Test get all meals.
        self.assertIsInstance(Meal.get_all(), list)
        self.assertEqual(1, len(Meal.get_all()))

        # Test deleting a meal.
        Meal.delete(id=1)
        self.assertEqual(None, Meal.get(id=1))
        self.assertEqual(0, len(Meal.get_all()))

    def test_order(self):
        '''Test order model.'''
        self.user1.add_user()
        self.meal1.add_meal()

        # Test saving an order
        id = self.order1.add_order()
        self.assertEqual(1, id)

        # Test getting a order.
        self.assertIsInstance(Order.get(id=1), tuple)

        # Test get all orders.
        self.assertIsInstance(Order.get_all(), list)

        # Test cost calculates correctly
        self.assertEqual(Order.total(order_id=1), 100)

        # Test deleting an order.
        Order.delete(id=1)
        self.assertEqual(None, Order.get(id=1))
        self.assertEqual(0, len(Order.get_all()))
