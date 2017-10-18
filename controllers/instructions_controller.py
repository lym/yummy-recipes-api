from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView

from models import (
    Instruction,
    Recipe,
)
from models.base_model import db as DB


class InstructionsController(MethodView):
    """ Controller for the instructions resource """
    def post(self):
        """ Instruction Creation """
        recipe_id   = int(request.get_json().get('recipe_id'))
        title       = request.get_json().get('title')
        description = request.get_json().get('description')

        # Check for required fields
        if recipe_id is None:
            abort(400)

        # Check if recipe for instruction exists
        existant_recipe = Recipe.query.filter_by(id=recipe_id).first()
        if existant_recipe is None:
            print('The recipe attached to instruction does not exist!')
            res = jsonify({'status': 400})
            abort(res)

        # Check if instruction already exists
        existant_instruction = Instruction.query.filter_by(
            title=title.lower()
        ).first()
        if ((existant_instruction is not None) and
                (existant_instruction.title == title.lower) and
                existant_instruction.recipe_id == recipe_id):
            print(
                'Oops! Instruction already exists and is attached to recipe {}'.format(recipe_id)  # NOQA
            )
            res = jsonify({'status': 400})
            abort(res)
        new_instruction = Instruction(
            recipe_id=recipe_id,
            title=title,
            description=description,
        )
        DB.session.add(new_instruction)
        DB.session.commit()
        res = {'status': 201}
        return jsonify(res)

    def get(self):
        """ Recipe retrieval """
        instructions = Instruction.query.all()
        content = []
        for instruction in instructions:
            record = {
                'id': instruction.id,
                'recipe_id': instruction.recipe.id,
                'user_id': instruction.recipe.user.id,
                'title': instruction.title,
                'description': instruction.description,
                'created': instruction.created,
                'modified': instruction.modified
            }
            content.append(record)
        res = jsonify(content)
        return res
