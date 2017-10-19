from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView

from models import (
    Ingredient,
    Recipe,
)
from models.base_model import db as DB


class IngredientsController(MethodView):
    """ Controller for the ingredients resource """
    def post(self):
        """ Ingredient Creation """
        recipe_id   = int(request.get_json().get('recipe_id'))
        title       = request.get_json().get('title')
        description = request.get_json().get('description')

        # Check for required fields
        if recipe_id is None:
            abort(400)

        # Check if recipe for ingredient exists
        existant_recipe = Recipe.query.filter_by(id=recipe_id).first()
        if existant_recipe is None:
            print('The recipe attached to ingredient does not exist!')
            res = jsonify({'status': 400})
            abort(res)

        # Check if ingredient already exists
        existant_ingredient = Ingredient.query.filter_by(
            title=title.lower()
        ).first()
        if ((existant_ingredient is not None) and
                (existant_ingredient.title == title.lower) and
                existant_ingredient.recipe_id == recipe_id):
            print(
                'Oops! Ingredient already exists and is attached to recipe {}'.format(recipe_id)  # NOQA
            )
            res = jsonify({'status': 400})
            abort(res)
        new_ingredient = Ingredient(
            recipe_id=recipe_id,
            title=title,
            description=description,
        )
        DB.session.add(new_ingredient)
        DB.session.commit()
        res = {'status': 201}
        return jsonify(res)

    def get(self):
        """ Recipe retrieval """
        ingredients = Ingredient.query.all()
        content = []
        for ingredient in ingredients:
            record = {
                'id': ingredient.id,
                'recipe_id': ingredient.recipe.id,
                'user_id': ingredient.recipe.user.id,
                'title': ingredient.title,
                'description': ingredient.description,
                'created': ingredient.created,
                'modified': ingredient.modified
            }
            content.append(record)
        res = jsonify(content)
        return res
