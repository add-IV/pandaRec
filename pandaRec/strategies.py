"""This module contains the ranking strategies used to rank recipes based on a query."""
from abc import ABC, abstractmethod
import json
import asyncio
from typing import TYPE_CHECKING
import websockets
from rapidfuzz import fuzz, process
from rapidfuzz.utils import default_process
from sentence_transformers import SentenceTransformer, util
from openai.embeddings_utils import get_embedding, cosine_similarity, get_embeddings
from .ml_embeddings import load_embeddings
from .search_index import (
    generate_search_index,
    load_search_index,
    lemmatize_no_stop_words,
)
from .context import Context
from .recipe import Recipe, RecipeResult, get_recipe_by_name

if TYPE_CHECKING:
    import nest_asyncio


class RankingStrategy(ABC):
    """An abstract class representing a ranking strategy."""

    @abstractmethod
    def search(
        self, context: Context, recipes: list[Recipe], num_results=10
    ) -> list[RecipeResult]:
        """Searches for recipes based on the context."""


class NameSearch(RankingStrategy):
    """A simple proof-of-concept ranking strategy that only
    searches for the query in the recipe name."""

    @staticmethod
    def search(  # pylint: disable=arguments-differ
        context: Context, recipes: list[Recipe]
    ) -> list[RecipeResult]:
        result = []
        for recipe in recipes:
            if context.query in recipe.name:
                result.append(RecipeResult(1, recipe))
        return result


class FuzzySearchName(RankingStrategy):
    """A fuzzy search ranking strategy that uses the name of the recipe."""

    @staticmethod
    def search(  # pylint: disable=arguments-differ
        context: Context, recipes: list[Recipe], num_results=10
    ) -> list[RecipeResult]:
        names = [recipe.name for recipe in recipes]
        matches: list[tuple[str, int]] = process.extract(
            context.query,
            names,
            scorer=fuzz.WRatio,
            limit=20,
            processor=default_process,
        )  # type: ignore
        result = [
            RecipeResult(score=match[1], recipe=get_recipe_by_name(match[0], recipes))
            for match in matches
        ]
        return result[:num_results]


class FuzzySearchDescription(RankingStrategy):
    """A fuzzy search ranking strategy that uses the description of the recipe."""

    def __init__(self, ratio=fuzz.partial_token_sort_ratio):
        """Initializes the fuzzy search ranking with a given rapidfuzz ratio."""
        super().__init__()
        self.ratio = ratio

    def search(
        self, context: Context, recipes: list[Recipe], num_results
    ) -> list[RecipeResult]:
        result = []
        for recipe in recipes:
            score = self.ratio(
                context.query, recipe.description, processor=default_process
            )
            result.append(RecipeResult(score, recipe))
        result.sort(key=lambda recipe_result: recipe_result.score, reverse=True)
        return result[:num_results]


class IndexSearch(RankingStrategy):
    """A ranking strategy that uses a search index to search for recipes."""

    def __init__(self, recipes: list[Recipe], path: str = ""):
        """The search index can be generated on the fly or loaded from a file."""
        super().__init__()
        if not path:
            self.index = generate_search_index(
                [recipe.description for recipe in recipes]
            )
        else:
            self.index = load_search_index(path)

    def search(
        self, context: Context, recipes: list[Recipe], num_results=10
    ) -> list[RecipeResult]:
        lemmatized_search = lemmatize_no_stop_words(context.query)

        # add 1 to the score for each word that is in the description (per recipe)
        scores = len(recipes) * [0]
        for word in lemmatized_search:
            for idx, _ in self.index.get(word, []):
                try:
                    scores[idx] += 1
                except IndexError:
                    print(idx)

        num_words = len(lemmatized_search)
        result = [
            RecipeResult(score / num_words, recipe)  # normalize score
            for score, recipe in zip(
                scores, recipes
            )  # scores and recipes are in the same order
        ]
        result.sort(key=lambda recipe_result: recipe_result.score, reverse=True)
        return result[:num_results]


class SemanticSearch(RankingStrategy):
    """A ranking strategy that uses semantic embeddings to search for recipes."""

    def __init__(
        self,
        recipes: list[Recipe],
        path: str = "",
        model: str = "sentence-transformers/all-mpnet-base-v2",
    ):
        """The embeddings can be generated on the fly or loaded from a file."""
        super().__init__()
        self.model = SentenceTransformer(model)
        descriptions = [recipe.description for recipe in recipes]
        if not path:
            self.embeddings = self.model.encode(descriptions)
        else:
            self.embeddings = load_embeddings(path)

    def search(
        self, context: Context, recipes: list[Recipe], num_results
    ) -> list[RecipeResult]:
        query_embedding = self.model.encode(context.query, convert_to_tensor=True)
        cos_scores = [
            util.cos_sim(query_embedding, embedding).item()  # type: ignore
            for embedding in self.embeddings
        ]
        result = [
            RecipeResult(score, recipe) for recipe, score in zip(recipes, cos_scores)
        ]
        result.sort(key=lambda recipe_result: recipe_result.score, reverse=True)
        return result[:num_results]


class OpenAIEmbeddings(RankingStrategy):
    """A ranking strategy that uses OpenAI embeddings to search for recipes."""

    def __init__(
        self,
        recipes: list[Recipe],
        path: str = "",
        model: str = "text-embedding-ada-002",
    ):
        """The embeddings can be generated on the fly or loaded from a file."""
        super().__init__()
        self.model = model
        descriptions = [recipe.description for recipe in recipes]
        if not path:
            self.embeddings = get_embeddings(descriptions, engine=self.model)
        else:
            self.embeddings = load_embeddings(path)

    def search(
        self, context: Context, recipes: list[Recipe], num_results
    ) -> list[RecipeResult]:
        if context.query == "":
            return []
        query_embedding = get_embedding(context.query, engine=self.model)
        cos_scores = [
            cosine_similarity(query_embedding, embedding)
            for embedding in self.embeddings
        ]
        result = [
            RecipeResult(score, recipe) for recipe, score in zip(recipes, cos_scores)
        ]
        result.sort(key=lambda recipe_result: recipe_result.score, reverse=True)
        return result[:num_results]


class WebSocketStrategy(RankingStrategy):
    """A ranking strategy that uses semantic embeddings to search for recipes."""

    def __init__(self):
        import nest_asyncio

        super().__init__()
        nest_asyncio.apply()

    async def asearch(
        self, context: Context, _recipes: list[Recipe], num_results
    ) -> str:
        """async search"""
        uri = "ws://localhost:8765"
        payload = json.dumps({"query": context.query, "num_results": num_results})
        async with websockets.connect(  # pylint: disable=no-member # type: ignore
            uri
        ) as websocket:
            await websocket.send(payload)
            result = await websocket.recv()
        return result

    def recipe_results_from_json(self, json_string: str) -> list[RecipeResult]:
        """recipes from json"""
        result = []
        recipe_results = json.loads(json_string)
        for recipe_result in recipe_results:
            recipe = Recipe.from_dict(recipe_result["recipe"])
            result.append(RecipeResult(recipe_result["score"], recipe))
        return result

    def search(self, context: Context, recipes: list[Recipe], num_results):
        text_result = asyncio.run(self.asearch(context, recipes, num_results))
        result = self.recipe_results_from_json(text_result)
        return result
