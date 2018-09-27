'''Orders model.'''
from os import getenv
from api.v2.connect_to_db import connect_to_db

conn=connect_to_db(getenv('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur=conn.cursor()

class Order(object):
    '''Order model.'''

    def __init__(self, user_id, meals_dict):
        '''
        Create an order.
        '''
        self.id = None

    def save(self):
        '''save item to db'''

        conn.commit()

    def add_order(self):
        '''Add order details to table.'''
        cur.execute(
            """
            INSERT INTO orders()
            VALUES()
            """,
            ()
        )
        self.save()

    @staticmethod
    def get(**kwargs):
        '''Get order by key'''
        for key, val in kwargs.items():
            query="SELECT * FROM orders WHERE {}='{}'".format(key,val)
            cur.excecute(query)
            order = cur.fetchone()
            return order

    @staticmethod
    def get_all():
        '''Get all orders.'''

        query="SELECT * FROM orders"
        cur.excecute(query)
        orders = cur.fetchall()
        return orders

    def delete_order(self):
        '''Delete an order from db.'''

        query = "DELETE FROM orders WHERE id={}".format(self.id)
        cur.execute(query)
        self.save()