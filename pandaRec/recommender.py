from ipydatagrid import DataGrid
from abc import ABC, abstractmethod
from .recipe import Recipe, RecipeResult
from dataclasses import dataclass

@dataclass
class Selection():
    r1: int
    c1: int
    r2: int
    c2: int


class context():
    selections: list[Selection]
    search: str


class SearchAlgorithm(ABC):
    @abstractmethod
    def search(self, context: context, recipes: list[Recipe]) -> list[RecipeResult]:
        pass

class Recommender():
    recipes: list[Recipe]
    context: context
    grid: DataGrid
    searchAlgorithm: SearchAlgorithm

