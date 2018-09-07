"""Models and their methods."""

from datetime import timedelta
from hashlib import sha256
from os import getenv
from time import time

from jwt import encode, decode

class DB():
    '''In memory database'''

    def __init__(self):
        '''Initialize db.'''
        
        self.users = {}
        self.orders = {}
        self.meals = {}
    
    def drop(self):
        self.__init__()            

db = DB()

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

        return getattr(db, cls.tablename).get(id)
        
    @classmethod
    def get_all(cls):
        '''Method to get all specified items from the db.'''

        return getattr(db, cls.tablename)
    
    @classmethod
    def get_by_key(cls, **kwargs):
        '''Method to get an item by key from the db.'''

        kwarg = kwargs.keys()[0]
        db_store = getattr(db, cls.tablename)
        
        for key in db_store:
            obj = db_store[key]
            if obj.view()[kwarg] == kwargs[kwarg]:
                return obj
        return None

    @classmethod
    def get_many_by_key(cls, **kwargs):
        '''Get many objects by key'''
        
        kwarg = list(kwargs.keys())[0]
        db_store = getattr(db, cls.tablename)
        objs = []
        for key in db_store:
            obj = db_store[key]
            if obj.view()[kwarg] == kwargs[kwarg]:
                objs.append(obj)
        return objs

class User(Base):
    '''Class for users: model and methods.'''

    tablename = 'users'

    def __init__(self, username, password, email):
        '''Initialize the user object.'''

        self.id = None
        self.username = username
        self.email = email
        self.password = self.make_hash(password)
        self.roles = []

    def make_hash(self, password):
        '''Generate hash of password.'''

        return sha256(password.encode('utf-8')).hexdigest()

    def generate_token(self):
        '''Method for generating user token.'''

        key = getenv('SECRET_KEY')
        payload = {'username': self.username,
                    'roles': self.roles,
                    'created_at': time(),
                    'exp': time() + timedelta(hours=7).total_seconds() }
        return encode(payload=payload, key=str(key), algorithm='HS256')
    
    @staticmethod
    def decode_token(token):
        '''Decode the generated user token.'''

        key = getenv('SECRET_KEY')
        return decode(token, key=key, algorithms=['HS256'])

    def check_password(self, password):
        '''validate password'''

        return True if self.make_hash(password) == self.password else False
    
    def view(self):
        '''Method for displaying user details.'''

        return {
            'username': self.username,
            'email': self.email,
            'roles': self.roles,
            'id': self.id
        }

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
        self.meals = [
            {'quantity': meals_dict[meal_id],
             'meal': Meal.get(id=meal_id).view()}
            for meal_id in meals_dict.keys()]
        self.user = User.get(id=user_id).view()
        self.time = time()
        self.total = self.get_total()

    def get_total(self):
        '''Method for calculating an order's total price.'''

        return sum([i['quantity'] * i['meal']['price'] for i in self.meals])

    def update(self, new_data):
        '''Method for updating details of an order.'''
        
        new_order = Order(
            new_data['user_id'], meals_dict=new_data['meals_dict'])
        setattr(new_order, 'id', self.id)
        return new_order.save()
