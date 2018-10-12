'''Models and their methods.'''

from datetime import timedelta
from hashlib import sha256
from os import getenv
from time import time

from jwt import encode, decode


class DB():
    '''In memory database.'''

    def __init__(self):
        '''Create an empty database.'''
        self.users = {}
        self.orders = {}
        self.meals = {}

    def drop(self):
        '''Drop entire database.'''
        self.__init__()


db = DB()


class Base:
    '''Base class to be inherited by other model classes.'''

    def save(self):
        '''Add object to database.'''
        if self.id is None:
            setattr(self, 'id', len(getattr(db, self.tablename)) + 1)
        getattr(db, self.tablename).update({self.id: self})
        return self.view()

    def delete(self):
        '''Delete object from database.'''
        del getattr(db, self.tablename)[self.id]

    def update(self, new_data):
        '''Update object.'''
        keys = new_data.keys()
        for key in keys:
            setattr(self, key, new_data[key])
        return self.save()

    def view(self):
        '''View object as a dictionary.'''
        return self.__dict__

    @classmethod
    def get(cls, id):
        '''Get object from it's table by id.'''
        return getattr(db, cls.tablename).get(id)

    @classmethod
    def get_all(cls):
        '''Get all objects in a table.'''
        return getattr(db, cls.tablename)

    @classmethod
    def get_by_key(cls, **kwargs):
        '''Get an object by a key that is not id.'''
        kwarg = list(kwargs.keys())[0]
        db_store = getattr(db, cls.tablename)
        for key in db_store:
            obj = db_store[key]
            if obj.view()[kwarg] == kwargs[kwarg]:
                return obj
        return None

    @classmethod
    def get_many_by_key(cls, **kwargs):
        '''Get an object by a key that is not id.'''
        kwarg = list(kwargs.keys())[0]
        db_store = getattr(db, cls.tablename)
        objs = []
        for key in db_store:
            obj = db_store[key]
            if obj.view()[kwarg] == kwargs[kwarg]:
                objs.append(obj)
        return objs


class User(Base):
    '''User model.'''

    tablename = 'users'

    def __init__(self, username, password, email):
        '''Initialize a user.'''
        self.id = None
        self.username = username
        self.email = email
        self.password = self.make_hash(password)
        self.roles = []

    def make_hash(self, password):
        '''Generate hash of password.'''
        return sha256(password.encode('utf-8')).hexdigest()

    def generate_token(self):
        '''Create a token for a user.'''
        key = getenv('APP_SECRET_KEY')
        payload = {
            'user_id': self.id,
            'username': self.username,
            'roles': self.roles,
            'created_at': time(),
            'exp': time() + timedelta(hours=7).total_seconds()}
        return encode(
            payload=payload, key=str(key), algorithm='HS256').decode('utf-8')

    @staticmethod
    def decode_token(token):
        '''View information inside a token.'''
        key = getenv('APP_SECRET_KEY')
        return decode(token, key=key, algorithms=['HS256'])

    def check_password(self, password):
        '''Validate a user's password.'''
        return True if self.make_hash(password) == self.password else False

    def view(self):
        '''View a user's information.'''
        return {
            'username': self.username,
            'email': self.email,
            'roles': self.roles,
            'id': self.id
        }

    @staticmethod
    def make_user_admin(user):
        '''Make a user an admin.'''
        user.roles.append('admin')
        user.save()


class Meal(Base):
    '''Meal model.'''

    tablename = 'meals'

    def __init__(self, name, price):
        '''Initialize a meal.'''
        self.id = None
        self.name = name
        self.price = price


class Order(Base):
    '''Order model.'''

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
             'meal': Meal.get(id=int(meal_id)).view()}
            for meal_id in meals_dict.keys()]
        self.user = User.get(id=user_id).view()
        self.completed = False
        self.accepted = False
        self.time = time()
        self.total = self.get_total()

    def get_total(self):
        '''Get total cost of an order.'''

        return sum([i['quantity'] * i['meal']['price'] for i in self.meals])

    def update(self, new_data):
        '''Update an order.'''

        new_order = Order(
            new_data['user_id'], meals_dict=new_data['meals_dict'])
        setattr(new_order, 'id', self.id)
        return new_order.save()
