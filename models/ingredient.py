from models.base_model import db as DB


class Ingredient(DB.Model):
    """ An ingredient belongs to a recipe """

    id = DB.Column(DB.Integer, primary_key=True)
    recipe_id = DB.Column(DB.Integer, DB.ForeignKey('recipe.id'))
    title = DB.Column(DB.String)
    description = DB.Column(DB.String)

    def __repr__(self):
        return "<Ingredient(ingredient_id='{}', recipe_id='{}', title='{}', description='{}')>".format(
                                self.id, self.recipe_id, self.title, self.description)
