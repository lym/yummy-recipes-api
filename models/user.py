from models.base_model import db as DB
from .timestamp_mixin import TimestampMixin


class User(TimestampMixin, DB.Model):
    __tablename__ = 'users'

    id          = DB.Column(DB.Integer, primary_key=True)
    first_name  = DB.Column(DB.String)
    last_name   = DB.Column(DB.String)
    username    = DB.Column(DB.String)
    email       = DB.Column(DB.String, unique=True)
    password    = DB.Column(DB.String)
    auth_token  = DB.Column(DB.String, nullable=False, unique=True)

    recipes = DB.relationship('Recipe', backref='user', lazy=True)

    def save(self):
        """ Takes care of creating a new user or updating a user instance
        TODO: Take care of update scenario
        """
        DB.session.add(self)
        DB.session.commit()

    def __repr__(self):
        return "<User(fullname='{}', email='{}', password='{}')>".format(
                                (self.first_name.capitalize() + ' ' + self.last_name.capitalize()),  # NOQA
                                self.email, self.password)
