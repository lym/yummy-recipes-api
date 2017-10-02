from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)
from .base_model import BaseModel


class Instruction(BaseModel):
    __tablename__ = 'instructions'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    title = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<Instruction(instruction_id='{}', recipe_id='{}', title='{}', description='{}')>".format(
                                self.id, self.recipe_id, self.title, self.description)
