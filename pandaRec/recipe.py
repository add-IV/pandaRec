from dataclasses import dataclass


@dataclass
class Recipe:
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
    score: float
    recipe: Recipe


@dataclass
class Embedding:
    name: str
    algorithm: str
    path: str
    model: str


@dataclass
class RecipeCollection:
    name: str
    description: str
    embeddings: list[Embedding]
    recipes: list[Recipe]


def get_recipe_by_name(name: str, recipes: list[Recipe]) -> "Recipe":
    return next((recipe for recipe in recipes if name == recipe.name))


def get_recipe_by_id(get_id: int, recipes: list[Recipe]) -> "Recipe | None":
    return next((recipe for recipe in recipes if get_id == recipe.id), None)
