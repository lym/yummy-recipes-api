from models.base_model import db as DB


class User(DB.Model):
    # __tablename__ = 'users'

    id          = DB.Column(DB.Integer, primary_key=True)
    first_name  = DB.Column(DB.String)
    last_name   = DB.Column(DB.String)
    username    = DB.Column(DB.String)
    email       = DB.Column(DB.String, unique=True)
    password    = DB.Column(DB.String)

    recipes = DB.relationship('Recipe', backref='user', lazy=True)


    def __repr__(self):
        return "<User(fullname='{}', email='{}', password='{}')>".format(
                                (self.first_name.capitalize() + ' ' + self.last_name.capitalize()),  # NOQA
                                self.email, self.password)
