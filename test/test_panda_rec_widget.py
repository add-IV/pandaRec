from pandarec.panda_rec_widget import (
    debounced,
    ResultWidget,
    PandaRecWidget,
    copy_button_html,
)
from pandarec import Recommender, strategies
from pandarec.recipe import RecipeResult, Recipe
import time
import ipywidgets as widgets
from pandas import DataFrame
from pandas.testing import assert_frame_equal


def test_copy_button_html():
    copy_button = copy_button_html("test")
    assert '<button class="copy_button"' in copy_button
    assert "onclick=navigator.clipboard.writeText('{}')".format("test") in copy_button


class TestDebounced:
    value = 0

    def fn(self):
        self.value += 1

    def test_debounced(self):
        debounced_test = debounced(0.1, self.fn)
        debounced_test()
        debounced_test()
        debounced_test()
        time.sleep(0.2)
        assert self.value == 1


class TestResultWidget:
    num_results = 10
    result_widget = ResultWidget(num_results, None)

    def test_result_widget(self):
        assert self.result_widget.num_results == self.num_results
        assert self.result_widget.copy_prefix == "widget.df."
        assert self.result_widget.copy_suffix == "\\nwidget.update_data()"
        assert len(self.result_widget.recipes) == self.num_results
        assert isinstance(self.result_widget.recipes[0]["name"], widgets.Label)
        assert isinstance(self.result_widget.recipes[0]["score"], widgets.Label)
        assert isinstance(self.result_widget.recipes[0]["code"], widgets.Label)
        assert isinstance(self.result_widget.recipes[0]["copy"], widgets.HTML)
        assert isinstance(
            self.result_widget.recipes[0]["description"], widgets.Textarea
        )

    def test_change_num_results(self):
        self.result_widget.change_num_results(20)
        assert self.result_widget.num_results == 20
        assert len(self.result_widget.recipes) == 20
        self.result_widget.change_num_results(self.num_results)

    def test_update(self):
        recipe = Recipe(1, "name", "description", "code", "keywords")
        recipeResult = RecipeResult(1, recipe)
        self.result_widget.update([recipeResult])
        assert self.result_widget.recipes[0]["name"].value == "name"
        assert self.result_widget.recipes[0]["score"].value == "1.00"
        assert self.result_widget.recipes[0]["code"].value == "code"
        assert self.result_widget.recipes[0]["description"].value == "description"
        copy_value = self.result_widget._modify_copy_text("code")
        assert self.result_widget.recipes[0]["copy"].value == copy_button_html(
            copy_value
        )

    def test_update_edge_cases(self):
        recipe = Recipe(1, "name", "description", "code", "keywords")
        recipeResult = RecipeResult(1, recipe)
        self.result_widget.update([recipeResult] * 20)
        assert len(self.result_widget.recipes) == self.num_results
        none_result = RecipeResult(1, None)  # type: ignore
        self.result_widget.update([none_result])


class TestPandaRecWidget:
    strategy = strategies.NameSearch()
    recommender = Recommender([], DataFrame(), strategy)  # type: ignore
    panda_rec_widget = PandaRecWidget(recommender)

    def test_panda_rec_widget(self):
        assert self.panda_rec_widget.recommender == self.recommender
        assert_frame_equal(self.panda_rec_widget.df, self.recommender.context.data)
        assert isinstance(self.panda_rec_widget.result_widget, ResultWidget)

    def test_setters(self):
        self.panda_rec_widget.options.children[1].value = "test"
        self.panda_rec_widget.set_copy_prefix(None)
        assert self.panda_rec_widget.result_widget.copy_prefix == "test"
        self.panda_rec_widget.options.children[3].value = "test2"
        self.panda_rec_widget.set_copy_suffix(None)
        assert self.panda_rec_widget.result_widget.copy_suffix == "test2"
        self.panda_rec_widget.options.children[5].value = "20"
        self.panda_rec_widget.set_num_results(None)
        assert self.panda_rec_widget.result_widget.num_results == 20

    def test_update_data(self):
        df = DataFrame({"a": [1, 2, 3, 4, 5], "b": [1, 2, 3, 4, 5]})
        self.panda_rec_widget.update_data(df)
        assert_frame_equal(self.panda_rec_widget.df, df)
        assert_frame_equal(self.panda_rec_widget.recommender.context.data, df)
