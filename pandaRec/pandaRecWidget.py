import ipywidgets as widgets
from IPython.display import clear_output
import ipydatagrid
from .recommender import Recommender
from .recipe import *
import os


class ResultWidget(widgets.GridBox):
    num_results = 20

    def __init__(self, num_results=20) -> None:
        super().__init__()
        self.layout = widgets.Layout(grid_template_columns="1fr 1fr 5fr", width="100%")
        self.num_results = num_results
        self.recipes = [
            [
                widgets.Label(),
                widgets.Label(),
                widgets.Textarea(layout=widgets.Layout(width="100%")),
            ]
            for _ in range(num_results)
        ]
        self.children = [item for sublist in self.recipes for item in sublist]
        print(self.children)

    def update(self, recipeResults: list[RecipeResult], recipes: list[Recipe]):
        for idx, recipeResult in enumerate(recipeResults):
            if idx >= self.num_results:
                continue
            recipe = get_recipe_by_id(recipeResult.recipeId, recipes)
            if recipe is not None:
                self.recipes[idx][0].value = recipe.name
                self.recipes[idx][1].value = str(recipeResult.score)
                self.recipes[idx][2].value = recipe.description
            else:
                self.recipes[idx][0].value = "Recipe not found"
                self.recipes[idx][1].value = ""
                self.recipes[idx][2].value = ""


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

        self.results_widget = ResultWidget(20)

        self.children = [self.data_grid, self.search_term_widget, self.results_widget]

    def update_recommendations(self, change):
        self.recommender.set_Search(str(self.search_term_widget.value))
        self.recommender.set_Selection(self.data_grid.selected_cells)
        self.recommender.recommend()
        self.results_widget.update(
            self.recommender.recommendedRecipes, self.recommender.recipes
        )
