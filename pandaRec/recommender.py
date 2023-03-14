from abc import ABC, abstractmethod
from .recipe import Recipe, RecipeResult
from dataclasses import dataclass
from pandas import DataFrame


@dataclass
class Selection:
    r1: int
    c1: int
    r2: int
    c2: int


class Context:
    selections: list[Selection]
    data: DataFrame
    search: str

    def __init__(self, selections: list[Selection], data: DataFrame, search: str):
        self.selections = selections
        self.data = data
        self.search = search

    def isWholeRow(self, selection: Selection) -> bool:
        return selection.c1 == 0 and selection.c2 == self.data.shape[1]

    def isWholeColumn(self, selection: Selection) -> bool:
        return selection.r1 == 0 and selection.r2 == self.data.shape[0]


class RecommendStrategy(ABC):
    @abstractmethod
    def search(self, context: Context, recipes: list[Recipe]) -> list[RecipeResult]:
        pass


class NameSearch(RecommendStrategy):
    @staticmethod
    def search(context: Context, recipes: list[Recipe]) -> list[RecipeResult]:
        result = []
        for recipe in recipes:
            if context.search in recipe.name:
                result.append(RecipeResult(1, recipe.id))
            else:
                result.append(RecipeResult(0, recipe.id))
        return result


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
