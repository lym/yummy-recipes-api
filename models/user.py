from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name  = Column(String)
    last_name   = Column(String)
    username    = Column(String)
    email       = Column(String)
    password    = Column(String)

    recipes = relationship('Recipe')


    def __repr__(self):
        return "<User(name='{}', fullname='{}', password='{}')>".format(
                                self.name, self.fullname, self.password)
