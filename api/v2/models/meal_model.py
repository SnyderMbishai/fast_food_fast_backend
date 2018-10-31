'''Meals model.'''

from os import getenv

from api.v2.connect_to_db import connect_to_db


conn = connect_to_db(getenv('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur = conn.cursor()


class Meal(object):
    '''Meal model.'''

    def __init__(self, name, price, img):
        '''Initialize a meal.'''
        self.id = None
        self.name = name
        self.price = price
        self.img = img

    def save(self):
        '''save item to db'''
        conn.commit()

    def add_meal(self):
        '''Add meal details to db table.'''
        cur.execute(
            """
            INSERT INTO meals(name, price, img)
            VALUES(%s,%s,%s)
            """,
            (self.name, self.price, self.img)
        )
        self.save()

    @staticmethod
    def get_all():
        '''Get all meals.'''
        query = "SELECT * FROM meals"
        cur.execute(query)
        meals = cur.fetchall()
        return meals

    @classmethod
    def get_cost(cls, meal_id, quantity=1):
        '''Calculate the cost of a meal given price and quantity'''
        price = cls.get(id=meal_id)[2]
        return price*quantity

    @classmethod
    def delete(cls, id):
        '''Delete a user from db.'''
        query = "DELETE FROM meals WHERE id={}".format(id)
        cur.execute(query)
        cls.save(cls)

    @classmethod
    def update(cls, id, new_data):
        '''Update meal details given new information.'''
        for key, val in new_data.items():
            cur.execute("""
            UPDATE meals SET {}='{}' WHERE id={}
            """.format(key, val, id))
            cls.save(cls)

    @staticmethod
    def get(**kwargs):
        '''Get meal by key'''
        for key, val in kwargs.items():
            query = "SELECT * FROM meals WHERE {}='{}'".format(key, val)
            cur.execute(query)
            user = cur.fetchone()
            return user

    @staticmethod
    def view(meal):
        '''View a meal information.'''
        return {
            'id': meal[0],
            'name': meal[1],
            'price': meal[2],
            'img_name': meal[3]
        }
