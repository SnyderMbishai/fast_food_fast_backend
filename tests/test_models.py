'''Test models.'''

from api.models import Meal, Order, User
from .base import BaseCase

class TestModels(BaseCase):
    '''Class for testing the user model.'''

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