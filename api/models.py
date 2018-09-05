"""Models and their methods."""

db = {}

class User(object):
    tablename = 'users'
    def __init__(self, username, password, email):
        self.id = None
        self.username = username
        self.email = email
        self.password = password
        self.roles = []

class Meal(object):
    
    tablename = 'meals'

    def __init__(self, name, price):
        self.id = None
        self.name = name
        self.price = price
