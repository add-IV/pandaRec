Getting Started
===============

.. _setup:

You can either clone this repo or use a Jupyter Notebook online service such as Binder:

- `Binder <https://mybinder.org/v2/gh/add-IV/pandaRec/master?labpath=examples%2Fexample_functionality.ipynb>`_
- `Google Colab <https://colab.research.google.com/github/add-IV/pandaRec/blob/master/examples/example_functionality.ipynb>`_
- Or clone the repo and install the requirements:
    1. git clone
    2. cd pandarec
    3. pip install -r requirements.txt (in a virtual environment)
    4. open the examples/example_functionality.ipynb notebook

Usage
-----

You can change the strategy at the top of the widget.
You can add a new strategy by inheriting from the RankingStrategy class.
You can find an overview over the current strategies in :ref:`strategies`.