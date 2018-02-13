import unittest
from models import Recipe


class TestRecipe(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_default_attributes(self):
        assert Recipe.__tablename__ is not None

    def create_test_recipe(self):
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
        recipe.save()

    def test_recipe_create(self):
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

    def test_create_duplicate_recipe(self):
        """It should reject duplicate recipes """
