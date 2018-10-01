'''User Model.'''

from datetime import timedelta
from hashlib import sha256

from os import getenv
from time import time
from jwt import encode, decode

from api.v2.connect_to_db import connect_to_db


conn = connect_to_db(getenv('APP_SETTINGS'))
print(conn)
conn.set_session(autocommit=True)
cur = conn.cursor()

class Roles:
    @staticmethod
    def get(**kwargs):
        '''Get role by name or id'''
        for key, val in kwargs.items():
            query = "SELECT * FROM roles WHERE {}='{}'".format(key, val)
            cur.execute(query)
            role = cur.fetchone()
            return role

class UserRoles:
    @staticmethod
    def get_user_roles(user_id):
        '''Get user roles  by user_id'''
        query = "SELECT role_id FROM user_roles WHERE user_id='{}'".format(user_id)
        cur.execute(query)
        role_ids = cur.fetchall()
        return [Roles.get(id=role_id[0])[1] for role_id in role_ids]


class User(object):
    '''User model.'''

    def __init__(self, username, password, email):
        '''Initialize a user.'''
        self.username = username
        self.email = email
        self.password = self.make_hash(password)

    def save(self):
        '''save item to db'''
        conn.commit()

    def add_user(self):
        '''Add user details to table.'''
        cur.execute(
            """
            INSERT INTO users (username, email, password)
            VALUES(%s,%s,%s)
            """,
            (self.username, self.email, self.password)
        )
        try:
            self.save()
            user = User.get(username=self.username)
            role = Roles.get(name='user')
            cur.execute(
                """
                INSERT INTO user_roles (user_id, role_id)
                VALUES(%s,%s)
                """,
                (user[0], role[0])
            )
            self.save()
        except Exception as e:
            raise e

    @staticmethod
    def get(**kwargs):
        '''Get user by key'''
        for key, val in kwargs.items():
            query="SELECT * FROM users WHERE {}='{}'".format(key,val)
            cur.execute(query)
            user = cur.fetchone()
            return user

    @staticmethod
    def get_all():
        '''Get all users.'''

        query="SELECT * FROM users"
        cur.execute(query)
        users = cur.fetchall()
        return users

    @classmethod
    def get_roles(cls, user_id):
        '''Get user roles.'''
        roles = UserRoles.get_user_roles(user_id=user_id)
        return roles

    def delete_user(self, id):
        '''Delete a user from db.'''
        query = "DELETE FROM users WHERE id={}".format(id)
        cur.execute(query)
        self.save()

    def make_hash(self, password):
        '''Generate hash of password.'''
        return sha256(password.encode('utf-8')).hexdigest()

    def generate_token(self, id):
        '''Create a token for a user.'''
        key = getenv('APP_SECRET_KEY')
        roles = User.get_roles(user_id=id)
        payload = {
            'user_id': id,
            'username': self.username,
            'roles': roles,
            'created_at': time(),
            'exp': time() + timedelta(hours=100).total_seconds()}
        return encode(
            payload=payload, key=str(key), algorithm='HS256').decode('utf-8')

    @staticmethod
    def decode_token(token):
        '''View information inside a token.'''
        key = getenv('APP_SECRET_KEY')
        return decode(token, key=key, algorithms=['HS256'])

    def check_password(self,username, password):
        '''Validate a user's password.'''
        user = User.get(username=username)
        return True if self.make_hash(password) == user[3] else False

    def view(self):
        '''View a user's information.'''
        id = User.get(username=self.username)
        return {
            'id':id,
            'username': self.username,
            'email': self.email
        }

    @staticmethod
    def make_user_admin(id):
        '''Superuser make user admin.'''
        user = User.get(id=id)
        user = User(username=user[1],password=user[2],email=user[3])
        user.assign_user_a_role('admin', id)

    def assign_user_a_role(self, role, user_id):
        '''assign user role'''
        role_id = Roles.get(name=role)[0]
        cur.execute(
            """
                INSERT INTO user_roles (user_id, role_id)
                VALUES(%s,%s)
                """,
            (user_id, role_id)
        )
        self.save()
