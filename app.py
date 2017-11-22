from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
from models.base_model import db
from controllers import (
    UsersController,
    UsersShowController,
    UserSearchController,
    LoginController,
    RecipesController,
    RecipesShowController,
    RecipeSearchController,
    InstructionsController,
    IngredientsController,
)

app = Flask('yummy_recipes_api')
app.config.from_object('settings.DevEnv')
db.app = app
db.init_app(app)
db.create_all()
api = Api(app)

migrate = Migrate(app, db)
CORS(app)  # Enable CORS on all our endpoints

api.add_resource(UsersController, '/users/')
api.add_resource(UsersShowController, '/users/<int:user_id>/')
api.add_resource(LoginController, '/login/')
api.add_resource(RecipesController, '/recipes/')
api.add_resource(RecipesShowController, '/recipes/<int:recipe_id>/')
api.add_resource(InstructionsController, '/instructions/')
api.add_resource(IngredientsController, '/ingredients/')
api.add_resource(UserSearchController, '/search/users')
api.add_resource(RecipeSearchController, '/search/recipes')
