from dataclasses import dataclass

class Recipe():
    id: int
    name: str
    description: str
    code: str
    keywords: str

    def __init__(self, id, name, description, code, keywords):
        self.id = id
        self.name = name
        self.description = description
        self.code = code
        self.keywords = keywords
    
    def __str__(self):
        return f"Recipe({self.id}, {self.name}, {self.description}, {self.code}, {self.keywords})"

@dataclass
class RecipeResult():
    score: float
    recipeId: int