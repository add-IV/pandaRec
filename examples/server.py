#!/usr/bin/env python

import asyncio
import sys
import json
import websockets

sys.path.append("../")
from pandarec.recipe import Recipe, RecipeResult
from pandarec.context import Context
from pandarec.strategies import SemanticSearch
from sentence_transformers import util


with open("../recipes/from_docstrings/recipes.json", "r") as file:
    recipes = json.load(file)

recipes = [Recipe.from_dict(recipe) for recipe in recipes]


class SemanticSearchNoSorting(SemanticSearch):
    def search_no_sort(self, context: Context, recipes: list[Recipe], num_results=10):
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


strategy = SemanticSearchNoSorting(
    recipes, path="../recipes/from_docstrings/embeddings.pt"
)


async def search(websocket):
    query = await websocket.recv()

    payload = json.loads(query)

    print(f"< {payload['query']}")

    context = Context(None, None, query)  # type: ignore

    result = strategy.search_no_sort(
        context, recipes, num_results=payload["num_results"]
    )

    payload = [
        {"score": recipe_result.score, "recipe": recipe_result.recipe.__dict__}
        for recipe_result in result
    ]

    print(f"> {json.dumps(payload)}")

    await websocket.send(json.dumps(payload))


async def main():
    async with websockets.serve(  # pylint: disable=no-member # type: ignore
        search, "localhost", 8765
    ):
        print("serving!")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    print("serving?")
    asyncio.run(main())
