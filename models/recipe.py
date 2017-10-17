from models.base_model import db as DB
from .timestamp_mixin import TimestampMixin


class Recipe(TimestampMixin, DB.Model):
    """ Encapsulates the business logic of a recipe in the yummy recipes
    system.
    A recipe belongs to a User
    """
    __tablename__ = 'recipes'

    id          = DB.Column(DB.Integer, primary_key=True)
    user_id     = DB.Column(DB.Integer, DB.ForeignKey('users.id'), nullable=False)
    title       = DB.Column(DB.String)
    description = DB.Column(DB.String)
    fulfilled   = DB.Column(DB.Boolean)

    instructions = DB.relationship('Instruction', backref='recipe', lazy=True)


    def __repr__(self):
        return "<Recipe(user_id='{}', title='{}', description='{}')>".format(
                                self.user_id, self.title, self.description)
