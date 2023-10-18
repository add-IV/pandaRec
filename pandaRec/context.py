"""Context classes for the pandas recommender.

This module contains the Context class,
which is used to represent the context of a search query."""

from dataclasses import dataclass  # type: ignore
from pandas import DataFrame


@dataclass
class Selection:
    """A class representing a rectangular selection of cells in a DataFrame.

    Attributes:
        r1 (int): The index of the first row in the selection.
        c1 (int): The index of the first column in the selection.
        r2 (int): The index of the last row in the selection.
        c2 (int): The index of the last column in the selection."""

    r1: int
    c1: int
    r2: int
    c2: int


@dataclass
class Context:
    """
    A class representing a context for a search query.

    Attributes:
        selections (list[Selection]):
            A list of Selection objects representing the selected cells in the DataFrame.
        data (DataFrame): The DataFrame being searched.
        query (str): The search query being used.
    """

    selections: list[Selection]
    data: DataFrame
    query: str

    def is_whole_row(self, selection: Selection) -> bool:
        """Returns True if the given Selection represents an entire row in the DataFrame."""
        return selection.c1 == 0 and selection.c2 == self.data.shape[1]

    def is_whole_column(self, selection: Selection) -> bool:
        """Returns True if the given Selection represents an entire column in the DataFrame."""
        return selection.r1 == 0 and selection.r2 == self.data.shape[0]
