# Expose V0.1 - Keynotes

## description of the domain

- data preparation
- pandas

## Problem Description

- data preparation is a time consuming task
- specialist knowledge is required
- software is not user friendly

## Solution

- code recommendations for data preparation with pandas

## Methods/ Libraries

- in jupyter notebook with pandas using ipydatagrid
- "recipies" for code recommendations
- possibly expansion into standalone jupyter extension/ vscode extension
  -> extendable
- should have less overhead than current options
- should be easy and fast to use

## Workpackages

### 1 Setup

- development of basic data structure for the code recommendations "recipies"
- importing regularly used data processing operations into this data structure
- basic ranking algorithm based on keyword matching/ some kind of search algorithm

### 2 Interface

- create interface for the code recommendations with ipydatagrid
- get current context of the data grid and use it to recommend code snippets
- get user search input and use it to recommend code snippets

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
