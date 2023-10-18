from dataclasses import dataclass  # type: ignore
from pandas import DataFrame


@dataclass
class Selection:
    r1: int
    c1: int
    r2: int
    c2: int


@dataclass
class Context:
    """
    A class representing a context for a search query.

    Attributes:
    -----------
    selections : list[Selection]
        A list of Selection objects representing the selected cells in the DataFrame.
    data : DataFrame
        The DataFrame being searched.
    query : str
        The search query being used.
    """

    selections: list[Selection]
    data: DataFrame
    query: str

    def is_whole_row(self, selection: Selection) -> bool:
        # Returns True if the given Selection object represents an entire row in the DataFrame.
        return selection.c1 == 0 and selection.c2 == self.data.shape[1]

    def is_whole_column(self, selection: Selection) -> bool:
        # Returns True if the given Selection object represents an entire column in the DataFrame.
        return selection.r1 == 0 and selection.r2 == self.data.shape[0]
