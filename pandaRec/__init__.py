"""Pandas Recommender

This package provides a recommender system for pandas DataFrames."""

from .panda_rec_widget import PandaRecWidget
from .recipe import Recipe, RecipeCollection, Embedding
from .recommender import Recommender
from . import strategies
from . import search_index
from . import ml_embeddings
