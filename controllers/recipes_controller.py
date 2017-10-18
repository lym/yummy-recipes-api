from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView

from models import (
    Recipe,
    User,
)
from models.base_model import db as DB


class RecipesController(MethodView):
    """ Controller for the user resource """
    def post(self):
        """ Recipe Creation """
        user_id = int(request.get_json().get('user_id'))
        title   = request.get_json().get('title')
        description = request.get_json().get('description')
        fulfilled   = request.get_json().get('fulfilled')

        # Check for required fields
        if user_id is None:
            abort(400)

        # Check if recipe owner exists
        existant_user = User.query.filter_by(id=user_id).first()
        if existant_user is None:
            print('Recipe owner does not exist!')
            res = jsonify({'status': 400})
            abort(res)

        # Check if recipe already exists
        existant_recipe = Recipe.query.filter_by(title=title.lower()).first()
        if ((existant_recipe is not None)and
                (existant_recipe.title == title.lower)):
            print('Recipe Already exists')
            res = jsonify({'status': 400})
            abort(res)
        new_recipe = Recipe(
            user_id=user_id,
            title=title,
            description=description,
            fulfilled=fulfilled
        )
        DB.session.add(new_recipe)
        DB.session.commit()
        res = {'status': 201}
        return jsonify(res)


    def get(self):
        """ Recipe retrieval """
        recipes = Recipe.query.all()
        content = []
        for recipe in recipes:
            record = {
                'id': recipe.id,
                'user_id': recipe.user.id,
                'title': recipe.title,
                'description': recipe.description,
                'created': recipe.created,
                'modified': recipe.modified
            }
            content.append(record)
        res = jsonify(content)
        return res
