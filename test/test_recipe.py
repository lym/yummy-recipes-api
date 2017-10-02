from models import Recipe


def test_default_attributes():
    assert Recipe.__tablename__ is not None


def test_recipe_create():
    """ It should create a new recipe """
    user_id = 123
    title = 'Test Recipe'
    description = 'This is a description for {}'.format(title)
    fulfilled = True

    recipe = Recipe(
        user_id=user_id,
        title=title,
        description=description,
        fulfilled=fulfilled,
    )

    assert recipe.user_id == user_id
    assert recipe.title == title
    assert recipe.description == description
    assert recipe.fulfilled == fulfilled
