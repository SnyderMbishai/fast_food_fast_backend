'''Orders model.'''

from os import getenv
from time import time

from api.v2.connect_to_db import connect_to_db
from api.v2.models.meal_model import Meal


conn = connect_to_db(getenv('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur = conn.cursor()


class Order:
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

    @staticmethod
    def get(**kwargs):
        '''Get order by key'''
        for key, val in kwargs.items():
            query = "SELECT * FROM orders WHERE {}='{}'".format(key, val)
            cur.execute(query)
            order = cur.fetchone()
            return order
    @staticmethod
    def get_all_by_user_id(user_id):
        '''Get orders belonging to a certain user'''
        query = "SELECT * FROM orders WHERE user_id='{}'".format(user_id)
        cur.execute(query)
        orders = cur.fetchall()
        return orders


    @staticmethod
    def get_meals(order_id):
        '''Get all meals of an order.'''
        cur.execute(
            """
            SELECT * FROM order_items WHERE order_id={}
            """.format(order_id))
        order_items = cur.fetchall()
        return [{
            "meal_id": item[1],
            "meal_name":Meal.get(id=item[1])[1],
            "order_item_id":item[0],
            "quantity":item[3]
        } for item in order_items]

    @staticmethod
    def view(order):
        '''View order details.'''
        order_id = order[0]
        user_id = order[1]
        completed = order[2]
        accepted = order[3]
        created_at = order[4]
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
        query = "SELECT * FROM orders"
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
    def update(cls, order_id, new_data):
        '''Method for updating order details.'''

        for item in new_data:
            meal_id, quantity = item['meal_id'], item['quantity']
            # lookup order_item
            cur.execute("""
                SELECT * FROM order_items WHERE meal_id='{}' AND order_id='{}'
            """.format(meal_id, order_id))
            order_item = cur.fetchone()
            if not order_item:
                cur.execute(
                    """
                    INSERT INTO order_items(order_id, meal_id, quantity)
                    VALUES({}, {}, {}) RETURNING id
                    """.format(order_id, meal_id, quantity)
                )
            else:
                if quantity <= 0:
                    # remove item
                    query = "DELETE FROM order_items WHERE order_id='{}' AND meal_id='{}'".format(order_id, meal_id)
                    cur.execute(query)
                else:
                    cur.execute("""
                    UPDATE order_items SET quantity='{}' WHERE order_id={} AND meal_id={}
                    """.format(quantity, order_id, meal_id))
            cls.save(cls)
            return cls.get(id=order_id)

    @classmethod
    def complete_order(cls, id):
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
