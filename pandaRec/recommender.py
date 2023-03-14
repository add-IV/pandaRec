from abc import ABC, abstractmethod
from .recipe import Recipe, RecipeResult
from dataclasses import dataclass
from pandas import DataFrame


@dataclass
class Selection:
    r1: int
    c1: int
    r2: int
    c2: int


class context:
    selections: list[Selection]
    data: DataFrame
    search: str

    def isWholeRow(self, selection: Selection) -> bool:
        return selection.c1 == 0 and selection.c2 == self.data.shape[1]

    def isWholeColumn(self, selection: Selection) -> bool:
        return selection.r1 == 0 and selection.r2 == self.data.shape[0]


class SearchAlgorithm(ABC):
    @abstractmethod
    def search(self, context: context, recipes: list[Recipe]) -> list[RecipeResult]:
        pass


class Recommender:
    recipes: list[Recipe]
    context: context
    searchAlgorithm: SearchAlgorithm
