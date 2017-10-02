from models import Ingredient


def test_default_attributes():
    assert Ingredient.__tablename__ is not None


def test_ingredient_create():
    """ It should create a new ingredient """
    recipe_id = 123
    title = "ingredient for recipe with id equal to {}".format(recipe_id)
    description = "This is a description of the '{}' recipe".format(title)

    ingredient = Ingredient(
        recipe_id=recipe_id,
        title=title,
        description=description,
    )

    assert ingredient.recipe_id == recipe_id
    assert ingredient.title == title
    assert ingredient.description == description
