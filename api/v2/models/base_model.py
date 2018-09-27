from os import getenv

from api.v2.connect_to_db import connect_to_db

conn=connect_to_db(getenv('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur=conn.cursor()

class BaseModel():
    '''Base class for models.'''

    def save(self):
        '''Save item.'''
        conn.commit()
    
    def close(self):
        '''close'''
        cur.close()
        conn.close()

    def get(self):
        '''Get item fom db.'''
        pass
    def delete(self):
        '''Delete Item from db.'''
        pass
    def update(self):
        '''Update Item details.'''
        pass
