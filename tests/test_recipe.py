import unittest
from pandaRec.recipe import Recipe, get_result_id, get_recipe_by_id


class createRecepies(unittest.TestCase):
    def test_createRecepies(self):
        recipe = Recipe(1, "name", "description", "code", "keywords")
        self.assertEqual(recipe.id, 1)
        self.assertEqual(recipe.name, "name")
        self.assertEqual(recipe.description, "description")
        self.assertEqual(recipe.code, "code")
        self.assertEqual(recipe.keywords, "keywords")
        self.assertEqual(str(recipe), "Recipe(1, name, description, code, keywords)")

    def test_from_dict(self):
        recipe = Recipe.from_dict(
            {
                "id": 1,
                "name": "name",
                "description": "description",
                "code": "code",
                "keywords": "keywords",
            }
        )
        self.assertEqual(recipe.id, 1)
        self.assertEqual(recipe.name, "name")
        self.assertEqual(recipe.description, "description")
        self.assertEqual(recipe.code, "code")
        self.assertEqual(recipe.keywords, "keywords")
        self.assertEqual(str(recipe), "Recipe(1, name, description, code, keywords)")


class testGetByIdOrName(unittest.TestCase):
    def test_get_result_id(self):
        recipes = [
            Recipe(1, "name", "description", "code", "keywords"),
            Recipe(2, "name2", "description2", "code2", "keywords2"),
        ]
        self.assertEqual(1, get_result_id("name", recipes))

    def test_get_recipe_by_id(self):
        recipe1 = Recipe(1, "name", "description", "code", "keywords")
        recipes = [recipe1, Recipe(2, "name2", "description2", "code2", "keywords2")]
        self.assertEqual(recipe1, get_recipe_by_id(1, recipes))


if __name__ == "__main__":
    unittest.main()
