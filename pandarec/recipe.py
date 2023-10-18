"""Recipe dataclass and related functions and classes."""
from dataclasses import dataclass


@dataclass
class Recipe:
    """A class representing a recipe."""

    id: int
    name: str
    description: str
    code: str
    keywords: str

    @staticmethod
    def from_dict(d: dict):
        return Recipe(**d)


@dataclass
class RecipeResult:
    """A class representing a recipe result."""

    score: float
    recipe: Recipe


@dataclass
class Embedding:
    """A class representing an embedding file with a specific strategy and model.

    Attributes:
        strategy: The strategy name of the embedding.
        path: The path of the embedding file.
        model: The model of the embedding."""

    path: str
    strategy: str
    model: str


@dataclass
class RecipeCollection:
    """A class representing a collection of recipes with a list of embeddings."""

    name: str
    description: str
    embeddings: list[Embedding]
    recipes: list[Recipe]


def get_recipe_by_name(name: str, recipes: list[Recipe]) -> Recipe:
    """Returns the recipe with the given name."""
    return next((recipe for recipe in recipes if name == recipe.name))


def get_recipe_by_id(get_id: int, recipes: list[Recipe]) -> Recipe:
    """Returns the recipe with the given ID."""
    return next((recipe for recipe in recipes if get_id == recipe.id))
