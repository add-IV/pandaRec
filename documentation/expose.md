# Expose V1: PandaRec - Recommendations for the Pandas Library

## Introduction

Code Recommendation in Software Development help developers write good code faster and easier, while optimally also suggesting solutions that are fast and easily maintainable. 

Pandas is a library for Python that helps with the effiicient cleaning, reshaping, visualization and merging of small or large datasets. While it is powerful and flexible, it is equally complex.

## Problem Description

Because of pandas complexity, it is hard to use for people without much programming knowledge in general and practice in data manipulation. In essence, the library has a sharp learning curve. 

## Solution

By recommending code snippets based on a search termn and specific information on the data, the learning curve should be flattened.

## Methods/ Libraries

Using jupyter notebooks we can create a gui that is easy to set up (e.g. in google colab) and recommmends predefined recipes/ snippets. The GUI should have an overview over the data with e.g. the ipydatagrid library. It should also have a search bar and the recommended code snippets. As long as this is kept expandable, this solution might be applied to other contexts, such as coding in an IDE with recommendations based on the current dataframes loaded and the current line as a search term. For recommending code snippets, different algorithms should be implemented and compared.

## Workpackages

The work can be grouped into the followeing Workpackages.

### 1 Setup

Development of a snippet data structure, importing of regularly used data processing operations into this data structure, preferably automated.

Development of a basic ranking algorithm such as keyword matching or a basic string search algorithm.

At this point we should have a usable base for implementing more complex features. The requirements for this Workpackage are only a working python installation and the pandas library.

### 2 Interface

Development of the interface by adding a table for the data, a search bar and space for the recommendations.

The current context should be linked to the recommender and the resulting snippets back to the gui.

This step will require a 


### 3 Improvements

- implementing multiple ranking algorithms
- improvement of "recipies" to recommend more complex operations
- autodetect pandas column types

### 4 Analysis

- compare different ranking algorithms based on speed and quality of the recommendations
- evaluation of different data structures for the "recipies"
- compare to different existing solutions

### 5 Extension

- extending the code recommendations to work without jupyter notebooks in vscode as an extension
- extension of the code recommendations to other libraries
