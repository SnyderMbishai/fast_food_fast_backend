## Fast Food Fast

[![Build Status](https://travis-ci.org/SnyderMbishai/fast_food_fast_backend.svg?branch=ch-update-readme-and-badges-160789023)](https://travis-ci.org/SnyderMbishai/fast_food_fast_backend)
[![Coverage Status](https://coveralls.io/repos/github/SnyderMbishai/fast_food_fast_backend/badge.svg?branch=ft-add-helpers-160346910)](https://coveralls.io/github/SnyderMbishai/fast_food_fast_backend?branch=ft-add-helpers-160346910)
[![Maintainability](https://api.codeclimate.com/v1/badges/c58e13d5bd032ed9dba9/maintainability)](https://codeclimate.com/github/SnyderMbishai/fast_food_fast_backend/maintainability)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)


### Link to heroku

https://fastfoodfastapi1n2.herokuapp.com/

### Documentation

https://fastfoodfastv2.docs.apiary.io/#

### Prerequisites

1. Python 3: https://www.python.org/downloads/
2. Flask: http://flask.pocoo.org/docs/1.0/installation/
3. Flask_restful: https://flask-restful.readthedocs.io/en/latest/installation.html
4. Pytest: https://docs.pytest.org/en/latest/getting-started.html
5. Postgresql: https://www.postgresql.org/
6. Psycopg2-binary: https://pypi.org/project/psycopg2-binary/

### Endpoints

| Endpoint                             | Method         | Description                         |
| ------------------------------------ | -------------- | ----------------------------------- |
| /api/v2/users/signup                 | POST           | signup a user                       |
| /api/v2/users/signin                 | POST           | signin a user                       |
| /api/v2/meals                        | POST           | create a meal                       |
| /api/v2/meals/<int:meal_id>          | GET/PUT        | get/edit a specific meal            |
| /api/v2/orders/                      | POST/GET       | creat order,get all orders          |
| /api/v2/orders/<int:order_id>        | PUT/GET/PATCH  | edit, get, complete an order        |
| /api/v2/orders/accept/<int:order_id> | PATCH          | accept or reject order              |

### Running and testing app

#### Running:

    $ virtualenv venv
    $ cd venv
    $ git clone https://github.com/SnyderMbishai/fast_food_fast_backend.git
    $ source venv/bin/activate
    $ cd fast_food_fast_backend
    $ export APP_SETTINGS=development
    $ export APP_SECRET_KEY="sdfghjklsdfghj"
    $ python run.py

###### examples of data that can be passed:

Registration:

    {
      "username": "Kazuri",
      "email": "kazuri@gmail.com",
      "password": "password123",
      "confirm password": "password123"
    }

Signup:

    {
      "username": "Kazuri",
      "password": "password123"
    }
Meal:

    {
      "name": "Ugali beef",
      "price": 500
    }

Order:

    {
      "user_id": 1,
      "meal_dict": {
        "1": 2
      }
    }

##### Testing

follow the steps above then:

    $ python -m pytest

### Author

Snyder Mbishai

### Contributions

This repo can be forked and contributed to.
