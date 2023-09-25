from abc import ABC, abstractmethod  # type: ignore
from .context import Context
from .recipe import *
from thefuzz import fuzz, process
from sentence_transformers import SentenceTransformer, util
from torch import save, load


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
                result.append(RecipeResult(1, recipe))
        return result


class FuzzySearchTitle(RecommendStrategy):
    @staticmethod
    def search(context: Context, recipes: list[Recipe]) -> list[RecipeResult]:
        titles = [recipe.name for recipe in recipes]
        matches: list[tuple[str, int]] = process.extract(context.search, titles, limit=20)  # type: ignore
        result = [
            RecipeResult(
                score=one_match[1], recipe=get_recipe_by_name(one_match[0], recipes)
            )
            for one_match in matches
        ]
        return result


class FuzzySearchDescription(RecommendStrategy):
    def __init__(self, ratio=fuzz.partial_ratio):
        super().__init__()
        self.ratio = ratio

    def search(self, context: Context, recipes: list[Recipe]) -> list[RecipeResult]:
        result = [
            RecipeResult(self.ratio(context.search, recipe.description), recipe)
            for recipe in recipes
        ]
        result.sort(key=lambda recipeResult: recipeResult.score, reverse=True)
        return result

class SemanticSearch(RecommendStrategy):
    def __init__(self, recipes: list[Recipe], path: str = None):
        super().__init__()
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        descriptions = [recipe.description for recipe in recipes]
        if not path:
            self.embeddings = self.model.encode(descriptions, convert_to_tensor=True)
        else:
            self.load_embeddings(path)

    def search(self, context: Context, recipes: list[Recipe]) -> list[RecipeResult]:
        query_embedding = self.model.encode(context.search, convert_to_tensor=True)
        cos_scores = [util.cos_sim(query_embedding, embedding).item() for embedding in self.embeddings]
        result = [RecipeResult(score, recipe) for recipe, score in zip(recipes, cos_scores)]
        result.sort(key=lambda recipeResult: recipeResult.score, reverse=True)
        return result

    def save_embeddings(self, path):
        save(self.embeddings, path)

    def load_embeddings(self, path):
        self.embeddings = load(path)