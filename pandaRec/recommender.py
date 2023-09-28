from .recipe import Recipe, RecipeResult
from pandas import DataFrame
from .context import Context, Selection
from .strategies import RecommendStrategy


class Recommender:
    recipes: list[Recipe]
    context: Context
    search_algorithm: RecommendStrategy
    recommended_recipes: list[RecipeResult]

    def __init__(
        self,
        recipes: list[Recipe],
        df: DataFrame,
        search_algorithm: RecommendStrategy,
    ):
        self.recipes = recipes
        self.context = Context([], df, "")
        self.search_algorithm = search_algorithm
        self.recommended_recipes = []

    def recommend(self):
        self.recommended_recipes = self.search_algorithm.search(
            self.context, self.recipes
        )

    def import_recipes(self, recipes: list[Recipe]):
        self.recipes = recipes

    def show_results(self) -> str:
        result = ""
        for recipe_result in self.recommended_recipes:
            result += f"{recipe_result.recipe.name}\t\tScore: {recipe_result.score}\n"
        return result

    def set_search(self, search: str):
        self.context.search = search

    def set_selection(self, selections: list[Selection]):
        self.context.selections = selections
