from models.base_model import db as DB
from .timestamp_mixin import TimestampMixin


class Instruction(TimestampMixin, DB.Model):
    """ A recipe consists of instructions (the steps one has to follow in order
    to prepare the meal). This class the contains the business logic of an
    instruction.
    """
    __tablename__ = 'instructions'

    id          = DB.Column(DB.Integer, primary_key=True)
    recipe_id   = DB.Column(DB.Integer, DB.ForeignKey('recipes.id'),
                            nullable=False)
    title       = DB.Column(DB.String)
    description = DB.Column(DB.String)

    def __repr__(self):
        return "<Instruction(instruction_id='{}', recipe_id='{}', title='{}', description='{}')>".format(  # NOQA
                                self.id, self.recipe_id, self.title, self.description)  # NOQA
