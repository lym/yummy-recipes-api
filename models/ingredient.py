from models.base_model import db as DB
from .timestamp_mixin import TimestampMixin


class Ingredient(TimestampMixin, DB.Model):
    """ An ingredient belongs to a recipe """
    __tablename__ = 'ingredients'

    id          = DB.Column(DB.Integer, primary_key=True)
    recipe_id   = DB.Column(
        DB.Integer, DB.ForeignKey('recipes.id'), nullable=False
    )
    title       = DB.Column(DB.String)
    description = DB.Column(DB.String)

    def __repr__(self):
        return "<Ingredient(ingredient_id='{}', recipe_id='{}', title='{}', description='{}')>".format(  # NOQA
                                self.id, self.recipe_id, self.title, self.description)  # NOQA
