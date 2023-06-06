from dataclasses import dataclass  # type: ignore
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

    def is_whole_row(self, selection: Selection) -> bool:
        return selection.c1 == 0 and selection.c2 == self.data.shape[1]

    def is_whole_column(self, selection: Selection) -> bool:
        return selection.r1 == 0 and selection.r2 == self.data.shape[0]
