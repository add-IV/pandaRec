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


def get_recipe_by_name(name: str, recipes: list[Recipe]) -> "Recipe":
    return next((recipe for recipe in recipes if name == recipe.name))


def get_recipe_by_id(id: int, recipes: list[Recipe]) -> "Recipe | None":
    return next((recipe for recipe in recipes if id == recipe.id), None)
