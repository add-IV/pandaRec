# Test set and sources

## setup

- name
- query
- list of recipes that would work
- perhaps list of recipes that would half work

## [PANDAS: Most used Functions in Data Science](https://scribe.rip/pandas-most-used-functions-in-data-science-51b7c2b9c38a)

### read file

Read a comma-separated values (csv) file into DataFrame.

### head

return the first 15 rows

### tail

return the last 18 rows

### info

Print a concise summary of a DataFrame.

### shape

Return a tuple representing the dimensionality of the DataFrame.

### size

Return an int representing the number of elements in this object.

### isna

total number of missing values
df.isna().sum()

### total unique values

get the total number of unique values in each column
df.nunique()

### value_counts

get the unique values of a single variable

### save to csv

save the dataframe to a csv file
df.to_csv('file_name.csv')

### columns

get the column names of the dataframe

## [30 Very Useful Pandas Functions for Everyday Data Analysis Tasks](https://regenerativetoday.com/30-very-useful-pandas-functions-for-everyday-data-analysis-tasks/)

### read_csv

Read a comma-separated values (csv) file into DataFrame.

### head

return the first 5 rows

### columns

see information about the columns

### drop

drop unnecessary columns

### len

get the length of the dataframe

### query

return rows that meet the condition

### iloc

get a subset of the dataframe using index

### loc

get a subset of the dataframe using labels

### dtypes

get the data types of all columns at once or for a single column

### select_dtypes

select all columns of a certain data type, exclude, include

### insert

insert a column at a specific location

### cumultaive sum

get the cumulative sum of a column

### sample

get a random sample of rows or columns from the dataframe

### where

query dataset based on condition

### unique

get unique values of a column, e.g. categorical

### nunique

get the number of unique values of a column

### rank

get the rank based on a column

### isin

get rows where a column value is in a list of values

### replace

replaces values by a different value

### rename

rename e.g. columns

### fillna

replace missing values with a value

### groupby

group data per a certain variable and find out useful information

### pct_change

get the percentage change between the current and a prior element

### count

the number of data in the specified direction

### value_counts

get the unique values of a single variable

### crosstab

cross tabulation frequency

### qcut

bins the data based on sample quantiles

### cut

bins the data based on values

### describe

get descriptive statistics of the dataframe

### nlargest and nsmallest

get the rows with the largest or smallest values of a variable

### explode

change a list-like column into rows
