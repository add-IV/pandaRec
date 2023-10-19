#!/usr/bin/env python
print("hi")

import asyncio
import json
import websockets
import sys


sys.path.append("../")
from pandarec.recipe import Recipe
from pandarec.context import Context
from pandarec.strategies import SemanticSearchFeedback


with open("../recipes/from_docstrings/recipes.json", "r") as file:
    recipes = json.load(file)

recipes = [Recipe.from_dict(recipe) for recipe in recipes]

print("loaded recipes")

strategy = SemanticSearchFeedback(
    recipes, path="../recipes/from_docstrings/embeddings.pt"
)

print("loaded strategy")


async def search(websocket):
    payload_string = await websocket.recv()
    payload = json.loads(payload_string)
    if payload["type"] == "search":
        print(f"< {payload['query']}")
        context = Context(None, None, payload_string)  # type: ignore
        result = strategy.search(context, recipes, num_results=payload["num_results"])
        payload = [
            {"score": recipe_result.score, "recipe": recipe_result.recipe.__dict__}
            for recipe_result in result
        ]
        print(f"> {json.dumps(payload)}")
        await websocket.send(json.dumps(payload))
    elif payload["type"] == "feedback":
        context = Context(None, None, payload["query"])  # type: ignore
        recipe = Recipe.from_dict(payload["recipe"])
        strategy.feedback(context, recipe, payload["positive"])
        strategy.save_feedback("feedback.txt")


async def main():
    async with websockets.serve(  # pylint: disable=no-member # type: ignore
        search, "localhost", 8765
    ):
        print("serving!")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    print("serving?")
    asyncio.run(main())
