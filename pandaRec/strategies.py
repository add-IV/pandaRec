from abc import ABC, abstractmethod  # type: ignore
from .context import Context
from .recipe import Recipe, RecipeResult


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
