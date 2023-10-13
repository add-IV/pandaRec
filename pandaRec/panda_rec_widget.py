import ipywidgets as widgets
from IPython.display import clear_output
import ipydatagrid
from .recommender import Recommender
from .recipe import *
from .copybutton import copybutton
import os
import traitlets as T


class ResultWidget(widgets.GridBox):
    num_results = 20
    copy_prefix = "widget.df."
    copy_suffix = "\nwidget.update_data()"

    def __init__(self, num_results) -> None:
        super().__init__()
        self.layout = widgets.Layout(
            grid_template_columns="2fr 1fr 4fr 1fr 16fr", width="100%"
        )
        self._change_num_results(num_results)
        self.update([])

    def _change_num_results(self, num_results):
        self.num_results = num_results
        self.recipes = []
        children = []
        for _ in range(num_results):
            self.recipes.append(
                {
                    "name": widgets.Label(),
                    "score": widgets.Label(),
                    "code": widgets.Label(),
                    "copy": copybutton(""),
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
                    self.recipes[-1]["copy"],
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
                self.recipes[idx]["copy"].set_copytext(
                    self.modify_copytext(recipeResult.recipe.code)
                )
                self.recipes[idx]["description"].value = recipeResult.recipe.description
            else:
                self.recipes[idx]["name"].value = "Recipe not found"
                self.recipes[idx]["score"].value = ""
                self.recipes[idx]["code"].value = ""
                self.recipes[idx]["copy"].set_copytext("")
                self.recipes[idx]["description"].value = ""

    def modify_copytext(self, copytext):
        return self.copy_prefix + copytext + self.copy_suffix


class PandaRecWidget(widgets.VBox):
    def __init__(
        self, recommender: Recommender, num_results=8, html=False, **kwargs
    ) -> None:
        super().__init__()

        self.recommender = recommender
        self.df = self.recommender.context.data

        print(kwargs)
        datagrid_layout = kwargs.pop("datagrid_layout", {})
        print(datagrid_layout)
        self.data_grid = ipydatagrid.DataGrid(
            self.recommender.context.data,
            editable=True,
            layout=widgets.Layout(**datagrid_layout),
        )

        self.search_box = widgets.Text(
            placeholder="Search term", description="Search:"
        )

        self.result_widget = ResultWidget(num_results)

        self.options = widgets.VBox(
            [
                widgets.Label("Copy Prefix"),
                widgets.Textarea(
                    value=self.result_widget.copy_prefix,
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.Label("Copy Suffix"),
                widgets.Textarea(
                    value=self.result_widget.copy_suffix,
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.Label("Number of results"),
                widgets.IntSlider(
                    value=self.result_widget.num_results,
                    min=1,
                    max=20,
                    step=1,
                ),
            ]
        )

        self.search_box.observe(self.update_recommendations, names="value")  # type: ignore
        self.data_grid.observe(self.update_recommendations, names="selected_cells")  # type: ignore

        self.options.children[1].observe(self.set_copy_prefix, names="value")  # type: ignore
        self.options.children[3].observe(self.set_copy_suffix, names="value")  # type: ignore
        self.options.children[5].observe(self.set_num_results, names="value")  # type: ignore

        self.extend_options = widgets.Accordion([self.options])
        self.extend_options.set_title(0, "Options")

        self._set_children()

    def set_copy_prefix(self, change):
        self.result_widget.copy_prefix = self.options.children[1].value  # type: ignore

    def set_copy_suffix(self, change):
        self.result_widget.copy_suffix = self.options.children[3].value  # type: ignore

    def set_num_results(self, change):
        self.result_widget._change_num_results(self.options.children[5].value)  # type: ignore
        self._set_children()
        self.update_recommendations(change)

    def _set_children(self):
        self.children = [
            self.extend_options,
            self.data_grid,
            self.search_box,
            self.result_widget,
        ]

    def update_recommendations(self, _change):
        self.recommender.set_search(str(self.search_box.value))
        self.recommender.set_selection(self.data_grid.selected_cells)
        self.recommender.recommend()
        self.result_widget.update(self.recommender.recommended_recipes)

    def update_data(self, df=None):
        if df is None:
            df = self.df
        self.data_grid = ipydatagrid.DataGrid(
            df, editable=True, layout=widgets.Layout()
        )
        self._set_children()
        self.data_grid.observe(self.update_recommendations, names="selected_cells")  # type: ignore
        self.df = df
        self.recommender.context.data = df
