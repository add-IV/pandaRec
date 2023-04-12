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
        return f"Recipe({self.id}, {self.name}, {self.description[0:99]}, {self.code}, {self.keywords})"

    @staticmethod
    def from_dict(d: dict):
        return Recipe(
            d["id"],
            d["name"],
            d["description"],
            d["code"],
            d["keywords"],
        )
    
    def show_as_result(self) -> str:
        return f"{self.name} ({self.id}): {self.description[0:99]}"


@dataclass
class RecipeResult:
    score: float
    recipeId: int
