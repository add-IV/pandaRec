import ipywidgets as widgets
from IPython.display import clear_output
import ipydatagrid
from .recommender import Recommender
from .recipe import *
import os
import traitlets as T


class ResultWidget(widgets.GridBox):
    num_results = 20

    def __init__(self, num_results=8) -> None:
        super().__init__()
        self.layout = widgets.Layout(
            grid_template_columns="2fr 1fr 2fr 9fr", width="100%"
        )
        self.num_results = num_results
        self.recipes = []
        children = []
        for _ in range(num_results):
            self.recipes.append(
                {
                    "name": widgets.Label(width="12.5%"),
                    "score": widgets.Label(width="6.25"),
                    "code": widgets.Label(width="12.5%"),
                    "description": widgets.Textarea(
                        layout=widgets.Layout(width="100%")
                    ),
                }
            )
            children.extend(
                [
                    self.recipes[-1]["name"],
                    self.recipes[-1]["score"],
                    self.recipes[-1]["code"],
                    self.recipes[-1]["description"],
                ]
            )
        self.children = children

    def update(self, recipeResults: list[RecipeResult]):
        for idx, recipeResult in enumerate(recipeResults):
            if idx >= self.num_results:
                break
            if recipeResult.recipe is not None:
                self.recipes[idx]["name"].value = recipeResult.recipe.name
                self.recipes[idx]["score"].value = f"{recipeResult.score:.2f}"
                self.recipes[idx]["code"].value = recipeResult.recipe.code
                self.recipes[idx]["description"].value = recipeResult.recipe.description
            else:
                self.recipes[idx]["name"].value = "Recipe not found"
                self.recipes[idx]["score"].value = ""
                self.recipes[idx]["code"].value = ""
                self.recipes[idx]["description"].value = ""


class PandaRecWidget(widgets.VBox):
    def __init__(self, recommender: Recommender) -> None:
        super().__init__()

        self.recommender = recommender
        self.df = self.recommender.context.data

        self.data_grid = ipydatagrid.DataGrid(
            self.recommender.context.data,
            editable=True,
            layout=widgets.Layout(),
        )

        self.search_term_widget = widgets.Text(
            placeholder="Search term", description="Search:"
        )

        self.search_term_widget.observe(self.update_recommendations, names="value")  # type: ignore
        self.data_grid.observe(self.update_recommendations, names="selected_cells")  # type: ignore

        self.results_widget = ResultWidget(20)

        self.children = [self.data_grid, self.search_term_widget, self.results_widget]

    def update_recommendations(self, change):
        self.recommender.set_search(str(self.search_term_widget.value))
        self.recommender.set_selection(self.data_grid.selected_cells)
        self.recommender.recommend()
        self.results_widget.update(self.recommender.recommended_recipes)

    def update_data(self, df=None):
        if df is None:
            df = self.df
        self.data_grid = ipydatagrid.DataGrid(
            df, editable=True, layout=widgets.Layout()
        )
        self.children = [self.data_grid, self.search_term_widget, self.results_widget]
        self.df = df
        self.recommender.context.data = df
