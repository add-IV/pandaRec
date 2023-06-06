import unittest
from pandaRec.context import Context, Selection
import pandas as pd
from pandas.testing import assert_frame_equal


class createContext(unittest.TestCase):
    def test_create_context(self):
        selections = []
        data = pd.DataFrame()
        search = ""
        context = Context(selections, data, search)
        self.assertEqual(context.selections, selections)
        assert_frame_equal(context.data, data)
        self.assertEqual(context.search, search)


class testIsWholeRowOrColumn(unittest.TestCase):
    def setUp(self):
        self.selections = []
        d = {'col1': [1, 2], 'col2': [3, 4]}
        self.data = pd.DataFrame(data=d, index=['row1', 'row2'])
        self.search = ""
        self.context = Context(self.selections, self.data, self.search)

    def test_is_whole_row(self):
        selection = Selection(0, 0, 1, 2)
        self.assertTrue(self.context.is_whole_row(selection))
    
    def test_is_whole_column(self):
        selection = Selection(0, 0, 2, 1)
        self.assertTrue(self.context.is_whole_column(selection))

    def test_is_not_whole_row(self):
        selection = Selection(0, 0, 1, 1)
        self.assertFalse(self.context.is_whole_row(selection))

    def test_is_not_whole_column(self):
        selection = Selection(0, 0, 1, 1)
        self.assertFalse(self.context.is_whole_column(selection))


if __name__ == "__main__":
    unittest.main()
