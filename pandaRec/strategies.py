from abc import ABC, abstractmethod  # type: ignore
from .context import Context
from .recipe import *
from thefuzz import fuzz, process


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
        return result


class FuzzySearchTitle(RecommendStrategy):
    @staticmethod
    def search(context: Context, recipes: list[Recipe]) -> list[RecipeResult]:
        titles = [recipe.name for recipe in recipes]
        extracted: list[tuple[str, int]] = process.extract(context.search, titles, limit=20)  # type: ignore
        result = [
            RecipeResult(one[1], getResultId(one[0], recipes)) for one in extracted
        ]
        return result


class FuzzySearchDescription(RecommendStrategy):
    def __init__(self, ratio=fuzz.partial_ratio):
        super().__init__()
        self.ratio = ratio

    def search(self, context: Context, recipes: list[Recipe]) -> list[RecipeResult]:
        result = [
            RecipeResult(self.ratio(context.search, recipe.description), recipe.id)
            for recipe in recipes
        ]
        result.sort(key=lambda recipeResult: recipeResult.score, reverse=True)
        return result
