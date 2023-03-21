from .recipe import Recipe, RecipeResult
from pandas import DataFrame
from .context import Context, Selection
from .strategies import RecommendStrategy


class Recommender:
    recipes: list[Recipe]
    context: Context
    recommendStrategy: RecommendStrategy
    recommendedRecipes: list[RecipeResult]

    def __init__(
        self,
        recipes: list[Recipe],
        df: DataFrame,
        searchAlgorithm: RecommendStrategy,
    ):
        self.recipes = recipes
        self.context = Context([], df, "")
        self.searchAlgorithm = searchAlgorithm
        self.recommendedRecipes = []

    def recommend(self):
        self.recommendedRecipes = self.searchAlgorithm.search(
            self.context, self.recipes
        )

    def importRecipes(self, recipes: list[Recipe]):
        self.recipes = recipes

    def showResults(self) -> str:
        result = ""
        for recipeResult in self.recommendedRecipes:
            recipe = next(
                (x for x in self.recipes if x.id == recipeResult.recipeId), None
            )
            result += f"{recipe}: {recipeResult.score}\n"
        return result

    def set_Search(self, search: str):
        self.context.search = search

    def set_Selection(self, selections: list[Selection]):
        self.context.selections = selections
