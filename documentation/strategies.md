# Strategies

This Document discusses a list of possible algorithms that can be used to solve the problem.

## Pattern

The solution will use a Strategy Pattern. The pattern is described in the [Strategy Pattern](https://en.wikipedia.org/wiki/Strategy_pattern) Wikipedia article.
Basically, the pattern allows to define a family of algorithms, encapsulate each one, and make them interchangeable. You can also mix and match the algorithms at runtime.

## Algorithms

### 1. Keyword matching

This algorithm compares the keywords of the recipe with the search terms. Depending on the number of matches, the recipe is ranked.

### 2. Fuzzy matching

This is more a combination of the keyword matching and the Levenshtein distance algorithm. The Levenshtein distance algorithm is used to calculate the distance between the search terms and the keywords of the recipe. The distance is used to rank the recipe. This approach might help in multiple algorithms.

### 7. Combination of algorithms

We can combine multiple algorithms to get the best results. For examlpe, using user feedback of a specific user in addition to the keyword matching algorithm will result in the user getting the result he wants for specific search terms.

### 4. User feedback

Based on the user feedback, we can rank the recipes. We can also collect which recipes are used the most and which are not used at all. This can be used to improve the ranking algorithm. The user feedback can be collected in a separate file.

### 3. Dataframe structure analysis

By analysing the the dataframe structure, such as column names, data types and values we can match them with the input of recipes. It might be even enhanced if we modify recipe to include argument types.

### 5. Web based algorithm

By offloading the ranking algorithm to a Server, we can improve the ranking algorithm over time. The ranking algorithm can be improved by collecting user feedback and by analysing the usage of the recipes. The ranking algorithm can be improved by using machine learning algorithms.

### 6. Machine learning

Training a model with user feedback, usage data and existing usage of the pandas library will probably give great results. However, this approach lives on the amount and quality of input data. Using a web based algorithm might help with collecting user data.

## Pros and cons of the algorithms

The specific pros and cons of the algorithms are not known yet. However, we can already make some assumptions on complexity and performance. The algorithms are arranged such that complexity in general increases going down the list. Since the solution will use a Strategy Pattern, we can easily switch between the algorithms and as such the goal will be to implement all of them.

## Analysing the effectiveness of the algorithms

The most important metric will probably be user feedback. However, this is also the most difficult to measure since the package probably wont be used by a lot of people during development. Contacting domain experts might provide critical feedback. I could also use synthetic data to simulate user behavior. Easier to measure will be speed and memory usage.