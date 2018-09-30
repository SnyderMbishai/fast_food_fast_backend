'''postgreql db connection'''

import os
from psycopg2 import connect


def connect_to_db(db=None):
    '''create a connection to the right db.'''
    if db == 'testing':
        db_name = os.getenv('TESTING_DB')
    else:
        db_name = os.getenv('DEV_DB')

    try:

        return connect(
            database=db_name,
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'))
        print('namds')
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
            password VARCHAR NOT NULL,
            roles BOOLEAN NOT NULL DEFAULT FALSE
        );
        """
    )


def roles(cur):
    '''Create user roles.'''

    cur.execute(
        """
        CREATE TABLE roles(
            id serial PRIMARY KEY,
            name VARCHAR NOT NULL);
        """
    )


# many to many user-role relationship
def user_roles(cur):
    '''Create user roles.'''
    cur.execute(
        """
        CREATE TABLE user_roles(
            user_id INTEGER,
            role_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
            constraint id PRIMARY KEY (user_id, role_id)
        );
        """
    )


def meals_table(cur):
    '''Define meals table.'''
    cur.execute(
        """
        CREATE TABLE meals(
            id serial PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE,
            price INTEGER NOT NULL
        );
        """
    )


def orders_table(cur):
    '''Define orders table.'''
    cur.execute(
        """
        CREATE TABLE orders(
            id serial PRIMARY KEY,
            user_id INTEGER NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT FALSE,
            accepted BOOLEAN NOT NULL DEFAULT FALSE,
            created_at FLOAT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )


def order_item(cur):
    '''Create order item.'''
    cur.execute(
        """
        CREATE TABLE order_items(
            id serial PRIMARY KEY,
            meal_id INTEGER NOT NULL,
            order_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        );
        """
    )


def make_roles(cur, conn):
    '''Add admin, user and superuser roles to the roles table.'''
    cur.execute("INSERT INTO roles(name)  VALUES('user')")
    cur.execute("INSERT INTO roles(name) VALUES('admin')")
    cur.execute("INSERT INTO roles(name) VALUES('superuser')")
    conn.commit()


def create(db=None):
    '''Create all required tables.'''
    conn = connect_to_db(db=db)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    cur.execute(
        """DROP TABLE IF EXISTS users, meals,orders, roles, user_roles, order_items CASCADE""")

    # create the tables
    user_table(cur)
    roles(cur)
    user_roles(cur)
    meals_table(cur)
    orders_table(cur)
    order_item(cur)
    make_roles(cur, conn)

    cur.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create()
