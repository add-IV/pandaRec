from dataclasses import dataclass


class Recipe:
    id: int
    name: str
    description: str
    code: str
    keywords: str

    def __init__(self, id: int, name: str, description: str, code: str, keywords: str):
        self.id = id
        self.name = name
        self.description = description
        self.code = code
        self.keywords = keywords

    def __str__(self) -> str:
        return f"Recipe({self.id}, {self.name}, {self.description}, {self.code}, {self.keywords})"

    @staticmethod
    def from_dict(d: dict):
        return Recipe(
            d["id"],
            d["name"],
            d["description"],
            d["code"],
            d["keywords"],
        )


@dataclass
class RecipeResult:
    score: float
    recipeId: int