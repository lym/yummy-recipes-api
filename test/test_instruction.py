from models import Instruction


def test_default_attributes():
    assert Instruction.__tablename__ is not None


def test_instruction_create():
    """ It should create a new instruction """
    recipe_id = 123
    title = "Instruction for recipe with id equal to {}".format(recipe_id)
    description = "This is a description of the '{}' recipe".format(title)

    instruction = Instruction(
        recipe_id=recipe_id,
        title=title,
        description=description,
    )

    assert instruction.recipe_id == recipe_id
    assert instruction.title == title
    assert instruction.description == description
