import unittest
from pandaRec.recommender import Recommender
from pandaRec.recipe import Recipe, RecipeResult
from pandaRec.strategies import NameSearch
import pandas as pd
from pandas.testing import assert_frame_equal
import yaml

recipesStr = """
- !!python/object:pandaRec.recipe.Recipe
  id: 1
  name: filter
  description: "Subset rows or columns of dataframe according to labels in the specified\
    index.\n\nNote that this routine does not filter a dataframe on its contents.\n\"
  code: ''
  keywords: ''
- !!python/object:pandaRec.recipe.Recipe
  id: 2
  name: backfill
  description: "Synonym for :meth:`DataFrame.fillna` with ``method='bfill'``.\n\n\
    Returns\n-------\nSeries/DataFrame or None\n    Object with missing values filled\
    or None if ``inplace=True``."
  code: ''
  keywords: ''
- !!python/object:pandaRec.recipe.Recipe
  id: 3
  name: fillna
  description: "Fill NA/NaN values using the specified method."
  code: ''
  keywords: ''
"""

class testRecommender(unittest.TestCase):
    def setUp(self):
        self.recipes = yaml.load(recipesStr, Loader=yaml.UnsafeLoader)

    def test_create_recommender(self):
        df = pd.DataFrame()
        searchAlgorithm = NameSearch()
        recommender = Recommender(self.recipes, df, searchAlgorithm)
        self.assertEqual(recommender.recipes, self.recipes)
        assert_frame_equal(recommender.context.data, df)
        self.assertEqual(recommender.searchAlgorithm, searchAlgorithm)
        self.assertEqual(recommender.recommendedRecipes, [])

    def test_recommend(self):
        df = pd.DataFrame()
        searchAlgorithm = NameSearch()
        recommender = Recommender(self.recipes, df, searchAlgorithm)
        recommender.set_search("fill")
        recommender.recommend()
        self.assertEqual(recommender.recommendedRecipes, [RecipeResult(score=1, recipeId=2), RecipeResult(score=1, recipeId=3)])


if __name__ == '__main__':
    unittest.main()