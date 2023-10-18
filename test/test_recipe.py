from pandarec.recipe import (
    Recipe,
    RecipeResult,
    Embedding,
    RecipeCollection,
    get_recipe_by_id,
    get_recipe_by_name,
)


class TestCreateRecepies:
    def test_createRecepies(self):
        recipe = Recipe(1, "name", "description", "code", "keywords")
        assert recipe.id == 1
        assert recipe.name == "name"
        assert recipe.description == "description"
        assert recipe.code == "code"
        assert recipe.keywords == "keywords"
        assert (
            str(recipe)
            == "Recipe(id=1, name='name', description='description', code='code', keywords='keywords')"
        )

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
        assert recipe.id == 1
        assert recipe.name == "name"
        assert recipe.description == "description"
        assert recipe.code == "code"
        assert recipe.keywords == "keywords"
        print(str(recipe))
        assert (
            str(recipe)
            == "Recipe(id=1, name='name', description='description', code='code', keywords='keywords')"
        )


class TestGetByIdOrName:
    def test_get_recipe_by_name(self):
        recipes = [
            Recipe(1, "name", "description", "code", "keywords"),
            Recipe(2, "name2", "description2", "code2", "keywords2"),
        ]
        assert recipes[0] == get_recipe_by_name("name", recipes)

    def test_get_recipe_by_id(self):
        recipe1 = Recipe(1, "name", "description", "code", "keywords")
        recipes = [recipe1, Recipe(2, "name2", "description2", "code2", "keywords2")]
        assert recipe1 == get_recipe_by_id(1, recipes)


def test_createEmbedding():
    embedding = Embedding("name", "algorithm", "path", "model")
    assert embedding.name == "name"
    assert embedding.strategie == "algorithm"
    assert embedding.path == "path"
    assert embedding.model == "model"
    assert (
        str(embedding)
        == "Embedding(name='name', algorithm='algorithm', path='path', model='model')"
    )


def test_createRecipeCollection():
    recipeCollection = RecipeCollection("name", "description", [], [])
    assert recipeCollection.name == "name"
    assert recipeCollection.description == "description"
    assert recipeCollection.embeddings == []
    assert recipeCollection.recipes == []
    assert (
        str(recipeCollection)
        == "RecipeCollection(name='name', description='description', embeddings=[], recipes=[])"
    )


def test_createRecipeResult():
    recipeResult = RecipeResult(
        1.0, Recipe(1, "name", "description", "code", "keywords")
    )
    assert recipeResult.score == 1.0
    assert recipeResult.recipe == Recipe(1, "name", "description", "code", "keywords")
    assert (
        str(recipeResult)
        == "RecipeResult(score=1.0, recipe=Recipe(id=1, name='name', description='description', code='code', keywords='keywords'))"
    )
