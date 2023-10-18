from pandaRec.context import Context, Selection
import pandas as pd
from pandas.testing import assert_frame_equal

def test_create_context():
    selections = []
    data = pd.DataFrame()
    search = ""
    context = Context(selections, data, search)
    assert context.selections == selections
    assert_frame_equal(context.data, data)
    assert context.query == search


class TestIsWholeRowOrColumn:
    selections = []
    d = {"col1": [1, 2], "col2": [3, 4]}
    data = pd.DataFrame(data=d, index=["row1", "row2"])
    search = ""
    context = Context(selections, data, search)

    def test_is_whole_row(self):
        selection = Selection(0, 0, 1, 2)
        assert self.context.is_whole_row(selection)

    def test_is_whole_column(self):
        selection = Selection(0, 0, 2, 1)
        assert self.context.is_whole_column(selection)

    def test_is_not_whole_row_end(self):
        selection = Selection(0, 0, 1, 1)
        assert not self.context.is_whole_row(selection)

    def test_is_not_whole_row_start(self):
        selection = Selection(1, 0, 2, 1)
        assert not self.context.is_whole_row(selection)

    def test_is_not_whole_column_end(self):
        selection = Selection(0, 0, 1, 1)
        assert not self.context.is_whole_column(selection)

    def test_is_not_whole_column_start(self):
        selection = Selection(0, 1, 1, 2)
        assert not self.context.is_whole_column(selection)