"""Models and their methods."""

from time import time

db = {}
class Base:
    '''Base class to be inherited by the models' classes'''

    def save(self):
        '''Method for saving objects to the db.'''

        if self.id is None:
            setattr(self, 'id', len(getattr(db, self.tablename)) + 1)
        getattr(db, self.tablename).update({self.id: self})
        return self.view()
    
    def delete(self):
        '''Method for deleting a db object.'''

        del getattr(db, self.tablename)[self.id]
    
    def update(self, new_data):
        '''Method for updating an objects' details'''

        keys = new_data.keys()
        for key in keys:
            setattr(self, key, new_data[key])
        return self.save()

    def view(self):
        '''Method for displaying an object's details.'''

        return self.__dict__
    
    @classmethod
    def get(cls, id):
        '''Method to get a specific item from the db.'''

        pass
        
    @classmethod
    def get_all(cls):
        '''Method to get all specified items from the db.'''

        pass
    
    @classmethod
    def get_by_key(cls, **kwargs):
        '''Method to get an item by key from the db.'''

        pass

class User(Base):
    '''Class for users: model and methods.'''

    tablename = 'users'

    def __init__(self, username, password, email):
        '''Initialize the user object.'''

        self.id = None
        self.username = username
        self.email = email
        self.password = password
        self.roles = []

class Meal(Base):
    '''Class for meals: model and methods.'''

    tablename = 'meals'

    def __init__(self, name, price):
        '''Initialize the meal object.'''

        self.id = None
        self.name = name
        self.price = price

class Order(Base):
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
