from models.base_model import db as DB


class Instruction(DB.Model):

    id          = DB.Column(DB.Integer, primary_key=True)
    recipe_id   = DB.Column(DB.Integer, DB.ForeignKey('recipe.id'),
                            nullable=False)
    title       = DB.Column(DB.String)
    description = DB.Column(DB.String)

    def __repr__(self):
        return "<Instruction(instruction_id='{}', recipe_id='{}', title='{}', description='{}')>".format(
                                self.id, self.recipe_id, self.title, self.description)
