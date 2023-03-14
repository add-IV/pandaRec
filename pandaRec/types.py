from ipydatagrid import DataGrid
from abc import ABC, abstractmethod
from dataclasses import dataclass

class Recipe():
    id: int
    name: str
    description: str
    code: str
    keywords: str

class Selection():
    r1: int
    c1: int
    r2: int
    c2: int
    w: int
    h: int
    
    def isWholeRow(self) -> bool:
        return self.r1 == self.r2 and self.c1 == 0 and self.c2 == self.w
    
    def isWholeColumn(self) -> bool:
        return self.c1 == self.c2 and self.r1 == 0 and self.r2 == self.h

class context():
    selections: list[Selection]
    search: str

@dataclass
class RecipeResult():
    recipeId: int
    score: float

class SearchAlgorithm(ABC):
    @abstractmethod
    def search(self, context: context, recipes: list[Recipe]) -> list[RecipeResult]:
        pass

class Recommender():
    recipes: list[Recipe]
    context: context
    grid: DataGrid
    searchAlgorithm: SearchAlgorithm

