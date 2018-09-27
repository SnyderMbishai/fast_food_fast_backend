'''User Model.'''

from datetime import timedelta
from hashlib import sha256
from os import getenv
from time import time

from jwt import encode, decode

from api.v2.connect_to_db import connect_to_db

conn=connect_to_db(getenv('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur=conn.cursor()

class User(object):
    '''User model.'''

    def __init__(self, username, password, email):
        '''Initialize a user.'''

        self.username = username
        self.email = email
        self.password = self.make_hash(password)
        # self.roles = []
    
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
            (self.username,self.email,self.password)
        )
        self.save()

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
        cur.excecute(query)
        users = cur.fetchall()
        return users
    
    def delete_user(self):
        '''Delete a user from db.'''

        query = "DELETE FROM users WHERE id={}".format(self.id)
        cur.execute(query)
        self.save()

    def make_hash(self, password):
        '''Generate hash of password.'''

        return sha256(password.encode('utf-8')).hexdigest()

    def generate_token(self):
        '''Create a token for a user.'''

        key = getenv('APP_SECRET_KEY')
        payload = {
            # 'user_id': self.id,
            'username': self.username,
            # 'roles': self.roles,
            'created_at': time(),
            'exp': time() + timedelta(hours=7).total_seconds()}
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
        return True if self.make_hash(user[3]) == self.password else False

    def view(self):
        '''View a user's information.'''

        return {
            'username': self.username,
            'email': self.email,
            # 'roles': self.roles,
            # 'id': self.id
        }

    @classmethod
    def add_role(role):
        '''Add user details to table.'''
        
        cur.execute(
            """
            INSERT INTO roles (name)
            VALUES(%s)
            """,
            (role)
        )
        conn.commit()
    
    def assign_user_a_role(self):
        '''assign user role'''
        pass

