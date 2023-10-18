"""Recommender class for PandaRec.

This module contains the Recommender class.
It is used to recommend recipes based on a given context."""
from pandas import DataFrame
from .recipe import Recipe, RecipeResult
from .context import Context, Selection
from .strategies import RankingStrategy


class Recommender:
    """A class representing a recommender.

    Attributes:
        context: The context.
        strategy: The strategy which is used to recommend recipes.
        recipes: The recipes to recommend.
        recommended_recipes: The result of the last recommendation."""

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

    def recommend(self, num_results=10):
        """Recommends recipes based on the current context."""
        self.recommended_recipes = self.strategy.search(
            self.context, self.recipes, num_results
        )

    def show_results(self, n=None) -> list[RecipeResult]:
        """Returns the recommended recipes.

        Args:
            n: The number of recipes to return. If None, all recipes are returned."""

        if n is None:
            return self.recommended_recipes
        return self.recommended_recipes[:n]

    def import_recipes(self, recipes: list[Recipe]):
        self.recipes = recipes

    def set_search(self, search: str):
        self.context.query = search

    def set_selections(self, selections: list[Selection]):
        self.context.selections = selections
