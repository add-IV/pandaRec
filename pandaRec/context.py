from dataclasses import dataclass
from pandas import DataFrame

@dataclass
class Selection:
    r1: int
    c1: int
    r2: int
    c2: int


class Context:
    selections: list[Selection]
    data: DataFrame
    search: str

    def __init__(self, selections: list[Selection], data: DataFrame, search: str):
        self.selections = selections
        self.data = data
        self.search = search

    def isWholeRow(self, selection: Selection) -> bool:
        return selection.c1 == 0 and selection.c2 == self.data.shape[1]

    def isWholeColumn(self, selection: Selection) -> bool:
        return selection.r1 == 0 and selection.r2 == self.data.shape[0]
