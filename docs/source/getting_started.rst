Getting Started
===============

.. _setup:

You can either clone this repo or use a Jupyter Notebook online service such as Google Colab.

- `Google Colab <https://colab.research.google.com/github/add-IV/pandaRec/blob/master/examples/example_functionality.ipynb>`_
- Or clone the repo and install the requirements:
    1. :code:`git clone https://github.com/add-IV/pandaRec.git`
    2. :code:`cd pandarec`
    3. :code:`pip install -r requirements.txt (in a virtual environment)`
    4. open the examples/example_functionality.ipynb notebook
    5. make sure to change the kernel to the virtual environment you created

Usage
-----

You can add a new strategy by inheriting from the RankingStrategy class.
You can find an overview over the current strategies in :ref:`strategies`.