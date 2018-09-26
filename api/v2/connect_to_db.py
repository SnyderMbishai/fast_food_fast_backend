'''postgreql db connection'''

import os 
from psycopg2 import connect

def connect_to_db(db=None):
    '''create a connection to the right db.'''

    if db=='testing':
        db_name = os.getenv('TESTING_DB')
    else:
        db_name= os.getenv('DEV_DB')
   
    try:
        return connect( 
            database=db_name,
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'))
    except:
        return('Unable to connect')

def user_table(cur):
    '''Define users table'''

    cur.execute(
        """
        CREATE TABLE users(
            id serial PRIMARY KEY,
            username VARCHAR NOT NULL UNIQUE,
            email VARCHAR NOT NULL UNIQUE ,
            password VARCHAR NOT NULL
        );
        """
    )

def meals_table(cur):
    '''Define meals table'''

    cur.execute(
        """
        CREATE TABLE meals(
            id serial PRIMARY KEY,
            meal_name VARCHAR NOT NULL UNIQUE,
            price INTEGER NOT NULL
        );
        """
    )  

def orders_table(cur):
    '''Define orders table.'''

    cur.execute(
        """
        CREATE TABLE orders(
            id serial PRIMARY KEY
        );
        """
    )

def create(db=None):
    conn = connect_to_db(db=db)
    print(conn)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS users, meals,orders CASCADE""")

    #create the tables
    user_table(cur)
    meals_table(cur)
    orders_table(cur)

    cur.close()
    conn.commit()
    conn.close()

if __name__=='__main__':
    create()
