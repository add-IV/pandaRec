from pandarec.recommender import Recommender
from pandarec.recipe import Recipe, RecipeResult
from pandarec.strategies import NameSearch
from pandarec.context import Selection
import pandas as pd
from pandas.testing import assert_frame_equal
import yaml

recipesStr = """
- !!python/object:pandarec.recipe.Recipe
  id: 1
  name: filter
  description: "Subset rows or columns of dataframe according to labels in the specified\
    index.\n\nNote that this routine does not filter a dataframe on its contents.\n\"
  code: ''
  keywords: ''
- !!python/object:pandarec.recipe.Recipe
  id: 2
  name: backfill
  description: "Synonym for :meth:`DataFrame.fillna` with ``method='bfill'``.\n\n\
    Returns\n-------\nSeries/DataFrame or None\n    Object with missing values filled\
    or None if ``inplace=True``."
  code: ''
  keywords: ''
- !!python/object:pandarec.recipe.Recipe
  id: 3
  name: fillna
  description: "Fill NA/NaN values using the specified method."
  code: ''
  keywords: ''
"""


class TestRecommender:
    recipes = yaml.load(recipesStr, Loader=yaml.UnsafeLoader)

    def test_create_recommender(self):
        df = pd.DataFrame()
        searchAlgorithm = NameSearch()
        recommender = Recommender(self.recipes, df, searchAlgorithm)
        assert recommender.recipes == self.recipes
        assert_frame_equal(recommender.context.data, df)
        assert recommender.strategy == searchAlgorithm
        assert recommender.recommended_recipes == []

    def test_recommend(self):
        df = pd.DataFrame()
        searchAlgorithm = NameSearch()
        recommender = Recommender(self.recipes, df, searchAlgorithm)
        recommender.set_search("fill")
        recommender.recommend()
        assert recommender.recommended_recipes == [
            RecipeResult(score=1, recipe=self.recipes[1]),
            RecipeResult(score=1, recipe=self.recipes[2]),
        ]

    def test_show_results(self):
        df = pd.DataFrame()
        searchAlgorithm = NameSearch()
        recommender = Recommender(self.recipes, df, searchAlgorithm)
        recommender.set_search("fill")
        recommender.recommend()
        assert recommender.get_results(1) == [
            RecipeResult(score=1, recipe=self.recipes[1])
        ]
        assert recommender.get_results() == [
            RecipeResult(score=1, recipe=self.recipes[1]),
            RecipeResult(score=1, recipe=self.recipes[2]),
        ]

    def test_setters(self):
        df = pd.DataFrame()
        searchAlgorithm = NameSearch()
        recommender = Recommender([], df, searchAlgorithm)
        recommender.import_recipes(self.recipes)
        recommender.set_search("fill")
        selections = [Selection(0, 0, 1, 1), Selection(0, 0, 1, 1)]
        recommender.set_selections(selections)
        assert recommender.context.query == "fill"
        assert recommender.context.selections == selections
        assert recommender.recipes == self.recipes
