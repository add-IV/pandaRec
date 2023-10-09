from .recipe import Recipe, RecipeResult
from pandas import DataFrame
from .context import Context, Selection
from .strategies import RankingStrategy


class Recommender:
    context: Context
    strategy: RankingStrategy
    recipes: list[Recipe]
    recommended_recipes: list[RecipeResult]

    def __init__(
        self,
        recipes: list[Recipe],
        df: DataFrame,
        strategy: RankingStrategy,
    ):
        self.recipes = recipes
        self.context = Context([], df, "")
        self.strategy = strategy
        self.recommended_recipes = []

    def recommend(self):
        self.recommended_recipes = self.strategy.search(self.context, self.recipes)

    def show_results(self, n=None) -> list[RecipeResult]:
        if n is None:
            return self.recommended_recipes
        return self.recommended_recipes[:n]

    def import_recipes(self, recipes: list[Recipe]):
        self.recipes = recipes

    def set_search(self, search: str):
        self.context.query = search

    def set_selection(self, selections: list[Selection]):
        self.context.selections = selections
