# Yummy Recipes API

API to the yummy recipes service

[![Build Status](https://travis-ci.org/lym/yummy-recipes-api.svg?branch=master)](https://travis-ci.org/lym/yummy-recipes-api)

## Features
### User signup/registration
Sample Request: `POST  http://127.0.0.1:5000/users/` with JSON payload
that looks something like:

    {
      "first_name": "Emma",
      "last_name": "Stone",
      "email": "ema@comics.com",
      "username": "ema",
      "password": "weakpass"
    }

Sample Response: {'status': 201}

### User index retrieval
Sample request: `GET  http://127.0.0.1:5000/users/`

Sample response:

    [
        {
            "email": "jdoe@anonpersons.com",
            "first_name": "Jane",
            "id": 1,
            "last_name": "Doe",
            "username": "jdoe"
        },
        {
            "email": "jsmith@anonmail.com",
            "first_name": "John",
            "id": 2,
            "last_name": "Wayasay",
            "username": "jsmith"
        },
        {
            "email": "jsmith200@anonmail.com",
            "first_name": "John",
            "id": 3,
            "last_name": "Smith",
            "username": "jsmith"
        },
        {
            "email": "ema@comics.com",
            "first_name": "Emma",
            "id": 7,
            "last_name": "Stone",
            "username": "ema"
        }
    ]

### User Login
Request format: `POST  http://127.0.0.1:5000/login/` with a JSON payload
like:

    {
      "email": "auth_user@realemail.com",
      "password": "weakpass"
    }

Sample Response:

    {
        "token": 1.74425898330645305300752607775784327253e+38
    }

## Development environment setup
### Project source code setup
- Clone this repository
- cd into the project directory
- Create a virtual environment
- Activate the virtual environment
- Run pip install against `requirements.txt`

### Database Setup
- Create a database in PostgreSQL for the project with:

    $ createdb yummy_recipes

- Login into the database, via psql for example, and create a <i>yummy
  recipes</i> user with the SQL statement:

    CREATE USER yummy_recipes WITH PASSWORD 'weakpass';

- Set the owner of the *yummy_recipes* database to this new user with
the SQL statement:

    ALTER DATABASE yummy_recipes OWNER TO yummy_recipes;

- Set up initial state of the database with:

     FLASK_DEBUG=3 FLASK_APP=app.py flask db upgrade

### Starting the API server
- Start the server with `FLASK_DEBUG=3 FLASK_APP=app.py flask run`
  (Debug level 3 for extra verbosity)

### Interacting with the server
- Issue requests against the server using a tool like <i>curl</i> or
  <i>postman</i>
