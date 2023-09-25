from .recipe import Recipe, RecipeResult
from pandas import DataFrame
from .context import Context, Selection
from .strategies import RecommendStrategy


class Recommender:
    recipes: list[Recipe]
    context: Context
    searchAlgorithm: RecommendStrategy
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

    def import_recipes(self, recipes: list[Recipe]):
        self.recipes = recipes

    def show_results(self) -> str:
        result = ""
        for recipeResult in self.recommendedRecipes:
            result += f"{recipeResult.recipe.show_as_result()}\t\tScore: {recipeResult.score}\n"
        return result

    def set_search(self, search: str):
        self.context.search = search

    def set_selection(self, selections: list[Selection]):
        self.context.selections = selections
