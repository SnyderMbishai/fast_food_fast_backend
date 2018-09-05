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
        


