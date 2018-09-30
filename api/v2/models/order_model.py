'''Orders model.'''

from os import getenv
from time import time

from api.v2.connect_to_db import connect_to_db
from api.v2.models.meal_model import Meal


conn=connect_to_db(getenv('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur=conn.cursor()

class Order(object):
    '''Order model.'''

    def __init__(self, user_id, meal_dict):
        '''
        Create an order.
        '''
        self.user_id = user_id
        self.created_at = time()
        self.meal_dict = meal_dict

    def save(self):
        '''save item to db'''
        conn.commit()

    def add_order(self):
        '''Add order details to table.'''
        cur.execute(
            """
            INSERT INTO orders(user_id, created_at)
            VALUES({}, {}) RETURNING id;
            """.format(self.user_id, self.created_at)
        )
        self.id = cur.fetchone()[0]
        self.save()
        self.make_order_items()
        return self.id

    def make_order_items(self):
        '''Add an order item.'''
        for key, val in self.meal_dict.items():
            cur.execute(
                """
                INSERT INTO order_items(order_id, meal_id, quantity)
                VALUES({}, {}, {}) RETURNING id
                """.format(self.id, key, val)
            )
            self.save()
            return id

    @staticmethod
    def get(**kwargs):
        '''Get order by key'''
        for key, val in kwargs.items():
            query="SELECT * FROM orders WHERE {}='{}'".format(key,val)
            cur.execute(query)
            order = cur.fetchone()
            return order

    @staticmethod
    def get_meals(order_id):
        '''Get all meals of an order.'''
        cur.execute(
            """
            SELECT * FROM order_items WHERE order_id={}
            """.format(order_id))
        order_items = cur.fetchall()
        return [{
            "meal_id":item[1],
            "order_item_id":item[0],
            "quantity":item[3]
        } for item in order_items]

    @staticmethod
    def view(order):
        '''View order details.'''
        order_id, user_id, completed, accepted, created_at = order[0], order[1], order[2], order[3], order[4]
        meals = Order.get_meals(order_id)
        total = Order.total(order_id)
        return {
            'order_id': order_id,
            'user_id': user_id,
            'completed': completed,
            'accepted': accepted,
            'created_at': created_at,
            'meals': meals,
            'total': total
        }

    @staticmethod
    def get_all():
        '''Get all orders.'''
        query="SELECT * FROM orders"
        cur.execute(query)
        orders = cur.fetchall()
        return orders

    @classmethod
    def delete(cls, id):
        '''Delete an order from db.'''
        query = "DELETE FROM orders WHERE id={}".format(id)
        cur.execute(query)
        cls.save(cls)

    @classmethod
    def total(cls, order_id):
        '''Calculate total cost of an order.'''
        order_items = cls.get_meals(order_id=order_id)
        cost = 0
        for order_item in order_items:
            cost += Meal.get_cost(meal_id=order_item["meal_id"], quantity=order_item["quantity"])
        return cost

    @classmethod
    def update(cls, id, new_data):
        '''Method for updating order details.'''
        for key, val in new_data.items():
            cur.execute("""
            UPDATE order_items SET {}='{}' WHERE order_id={}
            """.format(key, val, id))
            cls.save(cls)

    @classmethod
    def complete_order(cls,id):
        '''Method for completing an order'''
        cur.execute("""
                UPDATE orders SET completed='{}' WHERE id={}
                """.format(True, id))
        cls.save(cls)

    @classmethod
    def accept_order(cls, id, status):
        '''Method for accept/declining an order.'''
        cur.execute("""
                UPDATE orders SET accepted='{}' WHERE id={}
                """.format(status, id))
        cls.save(cls)
