from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from models.base_model import db
from controllers import (
    UsersController,
    LoginController,
)

""" Database Configuration """

DBHost       = 'localhost'
DBPort       = '5432'
DBName       = 'yummy_recipes'
DBUser       = 'yummy_recipes'
DBPass       = 'weakpass'

DATABASE_URL = "postgres://{}:{}@{}:{}/{}".format(
    DBUser,
    DBPass,
    DBHost,
    DBPort,
    DBName
)

app = Flask('yummy_recipes_api')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# db = SQLAlchemy(app)
db.app = app
db.init_app(app)
# db.create_all()
api = Api(app)
api.add_resource(UsersController, '/users/')
api.add_resource(LoginController, '/login/')
