"""Widget for PandaRec

This module contains the main UI for PandaRec. It is based on ipywidgets and
ipydatagrid.
"""
from threading import Timer
import ipywidgets as widgets
import ipydatagrid
from .recommender import Recommender
from .recipe import RecipeResult, Recipe


def debounced(wait, fn):
    """Decorator that will postpone a function's execution until after wait
    seconds have elapsed since the last time it was invoked. Modified from
    https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Events.html#debouncing
    """
    timer = None

    def decorated(*args, **kwargs):
        nonlocal timer

        def call_it():
            fn(*args, **kwargs)

        if timer is not None:
            timer.cancel()
        timer = Timer(wait, call_it)
        timer.start()

    return decorated


def copy_button_html(copy_text=""):
    """Returns HTML for a copy button."""
    return f"""
        <style>
            .copy_button:active {{
                background-color: var(--jp-success-color1);
            }}
        </style>
        <button class="copy_button" onclick=navigator.clipboard.writeText('{copy_text}') icon="copy">
            Copy
        </button>
        """


class ResultWidget(widgets.GridBox):
    """Widget for displaying the results of a search query.

    Attributes:
        num_results (int): The number of results to display.
        copy_prefix (str): The prefix to add to the code when copying.
        copy_suffix (str): The suffix to add to the code when copying."""

    num_results = 20
    copy_prefix = "widget.df."
    copy_suffix = "\\nwidget.update_data()"

    def __init__(self, num_results) -> None:
        super().__init__()
        self.layout = widgets.Layout(
            grid_template_columns="2fr 1fr 4fr 1fr 16fr", width="100%"
        )
        self.change_num_results(num_results)
        self.update([])

    def change_num_results(self, num_results):
        """Changes the number of results to display."""
        self.num_results = num_results
        self.recipes = []
        children = []
        for _ in range(num_results):
            self.recipes.append(
                {
                    "name": widgets.Label(),
                    "score": widgets.Label(),
                    "code": widgets.Label(),
                    "copy": widgets.HTML(copy_button_html(), button_style="primary"),
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

    def update(self, recipe_results: list[RecipeResult]):
        """Updates the results displayed by the widget."""
        for idx, recipe_result in enumerate(recipe_results):
            if idx >= self.num_results:
                break
            self._fill_with_values(self.recipes[idx], recipe_result)
        len_recipe_results = len(recipe_results)
        if len_recipe_results < self.num_results:
            for idx in range(len_recipe_results, self.num_results):
                self._fill_with_values(self.recipes[idx], RecipeResult(0, None))  # type: ignore

    def _fill_with_values(self, to_fill, recipe_result):
        if recipe_result.recipe is not None:
            to_fill["name"].value = recipe_result.recipe.name
            to_fill["score"].value = f"{recipe_result.score:.2f}"
            to_fill["code"].value = recipe_result.recipe.code
            to_fill["copy"].value = copy_button_html(
                self._modify_copy_text(recipe_result.recipe.code)
            )
            to_fill["description"].value = recipe_result.recipe.description
        else:
            to_fill["name"].value = "No Recipe Found"
            to_fill["score"].value = ""
            to_fill["code"].value = ""
            to_fill["copy"].value = copy_button_html()
            to_fill["description"].value = ""

    def _modify_copy_text(self, copy_text):
        return self.copy_prefix + copy_text + self.copy_suffix


class PandaRecWidget(widgets.VBox):
    """Widget for the main UI."""

    def __init__(
        self, recommender: Recommender, num_results=8, debounce=False, **kwargs
    ) -> None:
        """Initializes the PandaRecWidget.

        Args:
            recommender: The Recommender object to use.
            num_results: The number of results to display.
            debounce: Whether to debounce the search box.

        Keyword Args:
            datagrid_layout: The layout of the data grid."""
        super().__init__()

        self.recommender = recommender
        self.df = self.recommender.context.data
        if debounce:
            self.update_recommendations = debounced(
                0.5, self._base_update_recommendations
            )
        else:
            self.update_recommendations = self._base_update_recommendations

        datagrid_layout = kwargs.pop("datagrid_layout", {})
        self.data_grid = ipydatagrid.DataGrid(
            self.recommender.context.data,
            editable=True,
            layout=widgets.Layout(**datagrid_layout),
        )

        self.search_box = widgets.Text(placeholder="Search term", description="Search:")

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

        self.search_box.observe(self.update_recommendations, names="value")
        self.data_grid.observe(self.update_recommendations, names="selected_cells")

        self.options.observe(self.set_copy_prefix, names="children.1.value")
        self.options.observe(self.set_copy_suffix, names="children.3.value")
        self.options.observe(self.set_num_results, names="children.5.value")

        self.extend_options = widgets.Accordion([self.options])
        self.extend_options.set_title(0, "Options")

        self._set_children()

    def set_copy_prefix(self, _change):
        """Sets the prefix to add to the code when copying."""
        self.result_widget.copy_prefix = self.options.children[1].value  # type: ignore

    def set_copy_suffix(self, _change):
        """Sets the suffix to add to the code when copying."""
        self.result_widget.copy_suffix = self.options.children[3].value  # type: ignore

    def set_num_results(self, change):
        """Sets the number of results to display."""
        self.result_widget.change_num_results(self.options.children[5].value)  # type: ignore
        self._set_children()
        self.update_recommendations(change)

    def _set_children(self):
        self.children = [
            self.extend_options,
            self.data_grid,
            self.search_box,
            self.result_widget,
        ]

    def update_recommendations(self, _change):  # pylint: disable=method-hidden
        """Updates the recommendations displayed by the widget."""
        pass  # pylint: disable=unnecessary-pass

    def _base_update_recommendations(self, _change):
        self.recommender.set_search(str(self.search_box.value))
        self.recommender.set_selection(self.data_grid.selected_cells)
        self.recommender.recommend(self.result_widget.num_results)
        self.result_widget.update(self.recommender.recommended_recipes)

    def update_data(self, df=None):
        """Updates the DataFrame displayed by the widget."""
        if df is None:
            df = self.df
        self.data_grid = ipydatagrid.DataGrid(
            df, editable=True, layout=widgets.Layout()
        )
        self._set_children()
        self.data_grid.observe(self.update_recommendations, names="selected_cells")  # type: ignore
        self.df = df
        self.recommender.context.data = df
