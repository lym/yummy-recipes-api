# Yummy Recipes API

API to the yummy recipes service

[![Build Status](https://travis-ci.org/lym/yummy-recipes-api.svg?branch=master)](https://travis-ci.org/lym/yummy-recipes-api)

## Authentication
After registration, a user should obtain an auth token for use with
subsequent requests. The authentication token is passed in the header
section of resource requests. The authentication header takes the form:

    Authorization: Token <token value>

## Features
- User registration
- User token retrieval
- User list retrieval
- Recipe creation
- Recipe list retrieval
- Recipe instruction creation
- Instruction list retrieval
- Recipe ingredient creation
- Ingredient list retrieval

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

### User Login (Token retrieval)
Request format: `POST  http://127.0.0.1:5000/login/` with a JSON payload
like:

    {
      "email": "auth_user@realemail.com",
      "password": "weakpass"
    }

Sample Response:

    {
        "token": 6e4daedb5c452d5a3f9e30d332c651ad5a572111
    }


### User list retrieval
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
           ...
        }
    ]

### Individual user retrieval
Sample request: `GET  http://127.0.0.1:5000/users/<user_id>/`

Sample response:

    {
        "email": "jdoe@anonpersons.com",
        "first_name": "Jane",
        "id": 1,
        "last_name": "Doe",
        "username": "jdoe"
    }

### User Search
Clients have the ability to search users based on the name.

Sample request `GET http://127.0.0.1:5000/search/users?q=<search term>`

Sample response:

    [
        {
            "created": "Wed, 25 Oct 2017 18:05:29 GMT",
            "email": "lilk@badboyent.com",
            "first_name": "Lil",
            "id": 3,
            "last_name": "Kim",
            "modified": null,
            "username": "lilk"
        }
    ]

If no matches are found, an empty list/array is returned.

### User Deletion
Please note that a user may only delete their own user record. Also
deleting a user, purges all their recipes, instructions and ingredients.

Sample request: `DELETE  http://127.0.0.1:5000/users/<user_id>/`

Sample response:

    {
        "status": 204
    }


### Recipe creation
Sample request: `POST http://127.0.0.1:5000/recipes/` with a JSON
payload like:

    {
        "user_id": 1,
        "title": "First Recipe",
        "description": "This awesome recipe belongs to user with ID 1",
        "fulfilled": false
    }

Sample Response:

    {
      "status": 201
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
