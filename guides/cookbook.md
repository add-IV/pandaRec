# User Guides Made by the Library

## [Cookbook](https://pandas.pydata.org/docs/user_guide/cookbook.html#cookbook)

### Idioms

#### If-Then

- df.loc[<condition>, <column name>] = <value>
- sf.where(<condition>, <value>)
- df[<column name>] = df[<column name>].where(<condition>, <value>, <value2>)

#### Splitting

- df[df.<column name> < <value>]

#### Building Criteria

- sf.loc[(<condition>) & (<condition>), <column name>]
- sf.loc[(<condition>) | (<condition>), <column name>]
- sf.loc[(<condition>) & (<condition>), <column name>] = <value>
- sf.loc[(<condition>) | (<condition>), <column name>] = <value>
  
### Selection

- df[(df.<column name> < <value>>) & (df.index.isin(<list>))]
- label vs position based slicing
- ~ inverse of mask

#### New Columns

- df.loc[df.groupby(<column name>)[<column name>].idxmin()]
- df.sort_values(by=<column name>).groupby(<column name>, as_index=False).first()

### MultiIndexing

- df.set_index(<column name>)
- pd.MultiIndex.from_tuples(<list of tuples>)
- df.stack()

#### Slicing

- df.xs
- df.xs(<value>, level=<level>, axis=<axis>)
- All = slice(None)

#### Sorting

- df.sort_values(by=<column name>, ascending=<ascending>)

### Missing Data

- df.bfill()
- df.ffill()

### Grouping

- df.groupby(<column name>).apply(<function>)
- dg.get_group(<value>)
- replace with mean

#### Splitting

- df.groupby().agg()

### Timeseries

- dates.to_period(freq=<freq>).to_timestamp()

### Merge

- 
