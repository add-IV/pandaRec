import pandas as pd
import ipywidgets as widgets
from IPython.display import clear_output
import ipydatagrid
from .recommender import Recommender


class PandaRecWidget(widgets.VBox):
    def __init__(self, recommender: Recommender) -> None:
        super().__init__()

        self.recommender = recommender

        self.data_grid = ipydatagrid.DataGrid(
            self.recommender.context.data,
            editable=True,
            layout=widgets.Layout(height="100px"),
        )

        self.search_term_widget = widgets.Text(
            placeholder="Search term", description="Search:"
        )

        self.search_term_widget.observe(self.update_recommendations, names="value")  # type: ignore
        self.data_grid.observe(self.update_recommendations, names="selected_cells")  # type: ignore

        self.children = [self.data_grid, self.search_term_widget]

    def update_recommendations(self, change):
        self.recommender.set_Search(str(self.search_term_widget.value))
        self.recommender.set_Selection(self.data_grid.selected_cells)
        self.recommender.recommend()
        clear_output(wait=True)
        print(self.recommender.showResults())
