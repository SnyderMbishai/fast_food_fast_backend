'''Base test class.'''
from unittest import TestCase

from api.v2.models.meal_model import Meal
from api.v2.models.user_model import User
from api.v2.models.order_model import Order
from api.v2.connect_to_db import create, connect_to_db
from main import create_app


class BaseCase(TestCase):
    '''Base class to be inherited by all other testcases.'''

    def setUp(self):
        '''Set up test application.'''
        create('testing')

        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user1 = User(
            username='user1',
            email='user1@email.com',
            password='pass#123')
        self.meal1 = Meal(
            name='Meal1',
            price=100
        )
        self.meal1.save()
        self.order1 = Order(user_id=1, meal_dict={1:1})
        self.user_data_1 = {
            'username': 'user3',
            'email': 'user3@mail.com',
            'password': 'password',
            'confirm_password': 'password'
        }

        self.user_data_2 = {
            'username': '',
            'email': 'user2@mail.com',
            'password': 'password',
            'confirm_password': 'password'
        }

        self.user_data_3 = {
            'username': 'user3',
            'email': 'user3mail.com',
            'password': 'password',
            'confirm_password': 'password'
        }

        self.valid_meal_data = {
            'name': 'Meal2',
            'price': 100
        }
        self.valid_meal_data2 = {
            'name': 'Meal3',
            'price': 100
        }
        self.invalid_meal_data = {
            'name': None,
            'price': None
        }

    def get_user_token(self):
        '''Create a token for testing.'''
        self.user1.add_user()
        return self.user1.generate_token(id=1)

    def get_admin_token(self):
        '''Create an admin token for testing.'''

        admin = User(
            username='admin', password='pass1234', email='admin@mail.com')
        admin.add_user()
        admin_id = User.get(username='admin')[0]
        admin.assign_user_a_role('admin', admin_id)

        return admin.generate_token(id=admin_id)

    def get_super_user_token(self):
        superuser = User(username='Administrator',
                         password='pass400&', email='admin@admin.com')
        superuser.add_user()
        superuser_id = User.get(username='Administrator')[0]
        superuser.assign_user_a_role('superuser',superuser_id)

        return superuser.generate_token(id=superuser_id)

    def tearDown(self):
        '''Delete database and recreate it with no data.'''

        conn = connect_to_db('testing')
        cur = conn.cursor()
        cur.execute(
            """DROP TABLE IF EXISTS users, meals,orders, roles, user_roles, order_items CASCADE""")
        cur.close()
        conn.commit()
        conn.close()
