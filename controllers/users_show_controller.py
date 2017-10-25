from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView

from models import User
from models.base_model import db as DB
from .base_controller import BaseController


class UsersShowController(MethodView):
    """ Handles requests for a single user entity """
    def get(self, user_id):
        print('Requested User ID is: {}'.format(user_id))
        if not BaseController.authorized(request):
            abort(401)
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(404)
        record = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
            'created': user.created,
            'modified': user.modified
        }
        res = jsonify(record)
        return res

    def delete(self, user_id):
        """ Delete a user and all their instructions and ingredients """
        if not BaseController.authorized(request):
            abort(401)
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(404)

        # Ensure a user is deleting their own user record
        curr_user = BaseController.auth_user(request)
        if curr_user.id != user.id:
            abort(403)
        recipes = user.recipes
        if recipes != []:
            for recipe in recipes:
                instructions = recipe.instructions
                if instructions != []:
                    for instruction in instructions:
                        DB.session.delete(instruction)
                ingredients = recipe.ingredients
                if ingredients != []:
                    for ingredient in ingredients:
                        DB.session.delete(ingredient)
                DB.session.delete(recipe)
            DB.session.commit()
        DB.session.delete(user)
        DB.session.commit()
        res = {'status': 204}
        return jsonify(res)
