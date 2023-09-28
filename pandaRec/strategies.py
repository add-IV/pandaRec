from abc import ABC, abstractmethod  # type: ignore
from .context import Context
from .recipe import *
from thefuzz import fuzz, process
from sentence_transformers import SentenceTransformer, util
from .ml_embeddings import generate_embeddings_sentence_transformers, load_embeddings
from .lemmatize import (
    generate_search_index,
    load_search_index,
    get_lemmatized_no_stop_words,
)


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
        scores = len(recipes) * [0]
        words = context.search.split()
        for word in words:
            for idx in range(len(recipes)):
                scores[idx] += self.ratio(word, recipes[idx].description)
        scores = [score / len(words) for score in scores]
        result = [RecipeResult(score, recipe) for score, recipe in zip(scores, recipes)]
        result.sort(key=lambda recipe_result: recipe_result.score, reverse=True)
        return result


class IndexSearch(RecommendStrategy):
    def __init__(self, recipes: list[Recipe], path: str = "", ratio=fuzz.partial_ratio):
        super().__init__()
        if not path:
            self.index = generate_search_index(
                [recipe.description for recipe in recipes]
            )
        else:
            self.index = load_search_index(path)

    def search(self, context: Context, recipes: list[Recipe]) -> list[RecipeResult]:
        lemmatized_search = get_lemmatized_no_stop_words(context.search)
        scores = len(recipes) * [0]
        num_words = len(lemmatized_search)
        for word in lemmatized_search:
            if word in self.index:
                for idx, _ in self.index[word]:
                    scores[idx] += 1
        result = [
            RecipeResult(score / num_words, recipe)
            for score, recipe in zip(scores, recipes)
        ]
        result.sort(key=lambda recipe_result: recipe_result.score, reverse=True)
        return result


class SemanticSearch(RecommendStrategy):
    def __init__(self, recipes: list[Recipe], path: str = ""):
        super().__init__()
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        descriptions = [recipe.description for recipe in recipes]
        if not path:
            self.embeddings = generate_embeddings_sentence_transformers(descriptions)
        else:
            self.embeddings = load_embeddings(path)

    def search(self, context: Context, recipes: list[Recipe]) -> list[RecipeResult]:
        query_embedding = self.model.encode(context.search, convert_to_tensor=True)
        cos_scores = [util.cos_sim(query_embedding, embedding).item() for embedding in self.embeddings]  # type: ignore
        result = [
            RecipeResult(score, recipe) for recipe, score in zip(recipes, cos_scores)
        ]
        result.sort(key=lambda recipe_result: recipe_result.score, reverse=True)
        return result
