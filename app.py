from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from models.base_model import db
from controllers import (
    UsersController,
    UsersShowController,
    UserSearchController,
    LoginController,
    RecipesController,
    RecipesShowController,
    InstructionsController,
    IngredientsController,
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
db.create_all()
api = Api(app)

migrate = Migrate(app, db)

api.add_resource(UsersController, '/users/')
api.add_resource(UsersShowController, '/users/<int:user_id>/')
api.add_resource(LoginController, '/login/')
api.add_resource(RecipesController, '/recipes/')
api.add_resource(RecipesShowController, '/recipes/<int:recipe_id>/')
api.add_resource(InstructionsController, '/instructions/')
api.add_resource(IngredientsController, '/ingredients/')
api.add_resource(UserSearchController, '/search/users')
