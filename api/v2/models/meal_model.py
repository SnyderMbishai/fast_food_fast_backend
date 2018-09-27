'''Meals model.'''
from os import getenv

from api.v2.connect_to_db import connect_to_db

conn = connect_to_db(getenv('APP_SETTINGS'))
cur=conn.cursor()

class Meal(object):
    '''Meal model.'''

    def __init__(self, name, price):
        '''Initialize a meal.'''

        self.id = None
        self.name = name
        self.price = price

    def save(self):
        '''save item to db'''

        conn.commit()

    def add_meal(self):
        '''Add meal details to table.'''

        cur.execute(
            """
            INSERT INTO meals(name, price)
            VALUES(%s,%s)
            """,
            (self.name,self.price)
        )
        self.save()

    @staticmethod
    def get_all():
        '''Get all meals.'''

        query="SELECT * FROM meals"
        cur.execute(query)
        meals = cur.fetchall()
        return meals

    def delete_meal(self):
        '''Delete a user from db.'''

        query = "DELETE FROM meals WHERE id={}".format(self.id)
        cur.execute(query)
        self.save()

    @staticmethod
    def get(**kwargs):
        '''Get meal by key'''

        for key, val in kwargs.items():
            querry="SELECT * FROM meals WHERE {}='{}'".format(key,val)
            cur.execute(querry)
            user = cur.fetchone()
            return user

    def view(self):
        '''View a meal information.'''

        return {
            'id': self.id,
            'name': self.name,
            'price': self.price            
        }
