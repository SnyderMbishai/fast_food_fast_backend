"""Models and their methods."""

from time import time

db = {}

class User(object):
    '''Class for users: model and methods.'''

    tablename = 'users'

    def __init__(self, username, password, email):
        '''Initialize the user object.'''
        
        self.id = None
        self.username = username
        self.email = email
        self.password = password
        self.roles = []

class Meal(object):
    '''Class for meals: model and methods.'''

    tablename = 'meals'

    def __init__(self, name, price):
        '''Initialize the meal object.'''

        self.id = None
        self.name = name
        self.price = price

class Order(object):
    '''Class for orders: model and methods.'''

    tablename = 'orders'

    def __init__(self, user_id, meals_dict):
        '''
        Create an order.

        Pass in meals_dict as {meal_id: quantity}
        The user_id is the id of the user making the order.
        '''

        self.id = None
        self.meals_dict = meals_dict
        self.user_id = user_id
        self.time = time()
