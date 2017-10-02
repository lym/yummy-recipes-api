from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from .base_model import BaseModel


class Recipe(BaseModel):
    """ Encapsulates the business logic of a recipe in the yummy recipes
    system.
    A recipe belongs to a User
    """
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    fulfilled = Column(Boolean)
    instructions = relationship('Instruction')


    def __repr__(self):
        return "<Recipe(user_id='{}', title='{}', description='{}')>".format(
                                self.user_id, self.title, self.description)
