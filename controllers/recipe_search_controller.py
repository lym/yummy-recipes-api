from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView

from fuzzywuzzy import process

from models import Recipe
from .base_controller import (
    BaseController,
    RecipesEndpoint,
)


class RecipeSearchController(MethodView):
    """ Handles requests for a single recipe entity """
    def get(self):
        searched_query = request.args.get('q')
        if not BaseController.authorized(request):
            abort(401)

        # Run fuzzy search, Consider 50% good enough
        matched_recipes = []
        all_recipes = Recipe.query.all()
        for recipe in all_recipes:
            choices = [
                recipe.title + ' ' + recipe.description
            ]
            results = process.extract(searched_query, choices)
            if results is []:  # No matches found
                res = []
                return jsonify(res)
            for result in results:
                if result[1] > 50:
                    matched_recipes.append(recipe)
        content = []
        for matched_recipe in matched_recipes:
            record = {
                'id': matched_recipe.id,
                'user_id': matched_recipe.user_id,
                'title': matched_recipe.title,
                'description': matched_recipe.description,
                'created': matched_recipe.created,
                'modified': matched_recipe.modified,
                'links': {
                    'self': RecipesEndpoint + str(matched_recipe.id) + '/'
                }
            }
            content.append(record)
        return jsonify(content)
