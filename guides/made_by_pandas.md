# User Guides Made by the Library

## [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

### Viewing Data

- df.head
- df.tail
- df.index
- df.columns
- df.to_numpy
- df.describe
- df.T
- df.sort_index
- df.sort_values

### Selection

- df['A']
- df[0:3]
- df.loc
- df.iloc
- df.iat

#### Boolean Indexing

- df[df.A > 0]
- df[df > 0]
- df2[df2['E'].isin(['two', 'four'])]

#### Setting

- df.at
- df.iat
- df.loc

### Missing Data

- df.reindex
- df.dropna
- df.fillna
- pd.isna

### Operations

#### Stats

- df.mean
- df.mean(axis=1)
- df.sub

#### User Defined Function

- df.agg
- df.transform

#### Value Counts

- s.value_counts

#### String Methods

- s.str.lower
- s.str.___

### Merge

#### Concat

- pd.concat
  
#### Join

- df.merge

### Grouping

- df.groupby
  
### Reshaping

#### Stack

- pd.MultiIndex
- df.stack
- df.unstack

#### Pivot Tables

- df.pivot_table

#### Time Series

- s.resample
- s.tz_localize
- s.tz_convert

### Categoricals

- df['grade'] = df['grade'].astype('category')
- df['grade'].cat.categories = ['very good', 'good', 'very bad']
- df['grade'] = df['grade'].cat.set_categories(['very bad', 'bad', 'medium', 'good', 'very good'])
- df.sort_values(by='grade')
- df.groupby('grade').size()
- observed=False

### Plotting

- s.plot
- df.plot

### Importing & Exporting Data

#### CSV

- df.to_csv
- pd.read_csv

#### Parquet

- df.to_parquet
- pd.read_parquet

#### Excel

- df.to_excel
- pd.read_excel

### [Gotchas](https://pandas.pydata.org/docs/user_guide/gotchas.html#gotchas)
