# Polars

## EDA

```
# Get a mapping of column names to their data type
df.schema

# Get the dataframe's shape
df.shape

# Get list of column names
df.columns

# Get the first x rows of a dataset
df.head(3)

# Count number of rows
df.height

# Count number of columns
df.width

# Get info on dataset
df.describe()

# Counts dupe rows
df.is_duplicated()

# Counts number of unique rows
expr_unique_subset = pl.struct("a", "b").n_unique()

# Count null values per column
df.null_count()

# Count non-null values in each column
df.count()

# Count unique values in each group
df.group_by("d", maintain_order=True).n_unique()

# window function
orders = pl.scan_csv("orders.csv")
customers = pl.scan_csv("customers.csv")

orders_w_order_rank_column = (
    orders
    .join(customers, on="customer_id", how="left")
    .with_columns([
        pl.col("order_date_utc").rank()
        .over(pl.col("is_premium_customer"))
        .alias("order_rank")
    ])
)

(
    orders_w_order_rank_column
    .filter(pl.col("order_rank").le(2))
    .group_by(pl.col("is_premium_customer"))
    .agg(pl.col("order_value_usd").sum().name.prefix("sum_"))
    .collect()
)
```

## Update dataset

```
# Add blank columns to dataframe
df_final = df_select.with_columns(
    [
        pl.Series("schema_name", [None] * df.height),
        pl.Series("tables_used", [None] * df.height),
    ]
)

# Create new columns

    # create year column by extracting year from date column
    df_pl = df_pl.with_columns(pl.col("sales_date").dt.year().alias("year"))

    # create price column by dividing sales revenue by sales quantity
    df_pl = df_pl.with_columns((pl.col("sales_rev") / pl.col("sales_qty")).alias("price"))

    # create a column with a constant value
    df_pl = df_pl.with_columns(pl.lit(0).alias("dummy_column"))

# Add columns to dataframe by passing a list of expressions
df.with_columns(
    [
        (pl.col("a") ** 2).alias("a^2"),
        (pl.col("b") / 2).alias("b/2"),
        (pl.col("c").not_()).alias("not c"),
    ]
)

# Sort by one column
df.sort('A')

# Sort by multiple columns
df.sort("c", "a", descending=[False, True])

# Set column names
df.columns = ["apple", "banana", "orange"]

# Fill floating point NaN value with a fill value
df.with_columns(pl.col("b").fill_nan(0))

# Fill all na's
df.fill_none(value)

# Filter the expression based on one or more predicate expressions.
# The original order of the remaining elements is preserved.
# Elements where the filter does not evaluate to True are discarded, including nulls.
df.group_by("group_col").agg(
    lt=pl.col("b").filter(pl.col("b") < 2).sum(),
    gte=pl.col("b").filter(pl.col("b") >= 2).sum(),
).sort("group_col")

# Replace multiple values by passing sequences to the old and new parameters
df.with_columns(replaced=pl.col("a").replace([2, 3], [100, 200]))

# Transpose data
df.transpose(include_header=True)

# Remove columns from df
df.drop(["bar", "ham"])

# Drop a subset of columns, as defined by name or with a selector
df.drop_nulls(subset=cs.integer())

# Rename columns
df.rename({"foo": "apple"})

# Add column showing % change between rows
df.with_columns(pl.col("a").pct_change().alias("pct_change"))

# Choose columns to include in output
# single
df.select('A')

# double
df.select('A', 'B')

# Sum multiple columns
df.select(pl.sum("a", "c"))

# Sum all values horizontally across columns
df.with_columns(sum=pl.sum_horizontal("a", "b"))

# Count the occurrences of unique values in a column
df.select(pl.n_unique("b", "c"))

# Generate an index column by using len in conjunction with int_range()
df.select(
    pl.int_range(pl.len(), dtype=pl.UInt32).alias("index"),
    pl.all(),
)

# Get the maximum value horizontally across columns
df.with_columns(max=pl.max_horizontal("a", "b"))

# Round the values as specified and format as currency
df = df.with_columns([
    pl.col('Risk').round(2).map_elements(lambda x: f"${x:,.2f}", return_dtype=pl.Utf8)])

# Update data types for multiple columns
filtered_df = df.with_columns([
    pl.col("dot_number__c").cast(pl.Int64),
    pl.col("mc_number__c").cast(pl.Int64),
    pl.col("physphonenbr").cast(pl.Int64),
    pl.col("trucknbr").cast(pl.Int64)
])

# change the data type of sales date from string to date
df_pl = df_pl.with_columns(pl.col("sales_date").str.to_date())

# merge 2 datasets
df1.join(df2, on='key')

# merge >2 datasets
df1.join(df2, on='key').join(df3, on='key')

# concatenate dataframes
pl.concat([df1, df2])

# Sort columns
df.select(sorted(df.columns))

# Sort columns in reverse order
df.select(sorted(df.columns, reverse=True))

# Select columns based on headers
q = (
    pl.scan_csv('Titanic_train.csv')
    .select(
        ['Name','Age']
    )
)
q.collect()

# Exclude only one column
q = (
    pl.scan_csv('Titanic_train.csv')
    .select(
        pl.exclude('PassengerId')
    )
)
q.collect()

# Select columns based on string

q = (
    pl.scan_csv('Titanic_train.csv')
    .select(
        pl.col('^S.*$')  # get all columns that starts with S
    )
)
q.collect()

# Split columns
# Part 1
q = (
    pl.scan_csv('names.csv')
    .select(
    [
        'name',
        pl.col('name').str.split(' ').alias('splitname'),
        'age',
    ])
)
q.collect()

# Part 2
q = (
    pl.scan_csv('names.csv')
    .select(
    [
        'name',
        pl.col('name').str.split(' ').alias('split_name'),
        'age',
    ])
    .with_column(
        pl.struct(
            [
                pl.col('split_name').arr.get(i).alias(
                    'first_name' if i==0 else 'last_name') 
                for i in range(2)
            ]
        ).alias('split_name')
    )
)
q.collect()
```

## Categorical Filters and queries 

```
# basic filters
    # sales quantity is more than 0
    df_pl.filter(pl.col("sales_qty") > 0)

    # store code is B1
    df_pl.filter(pl.col("store_code") == "B1")

    # sales quantity is more than 0 and store code is A2
    df_pl.filter((pl.col("store_code") == "A2") & (pl.col("sales_qty") > 0))

    # product code is one of the following: 89909, 89912, 89915, 89918
    df_pl.filter(pl.col("product_code").is_in([89909, 89912, 89915, 89918]))

# Replace all matching regex/literal substrings with a new string value
df.with_columns(pl.col("text").str.replace_all("a", "-"))

# apply case-insensitive string replacement
df.with_columns(
    pl.col("weather").str.replace_all(
        r"(?i)foggy|rainy|cloudy|snowy", "Sunny"
    )
)

# split text to columns using delimiter
df.with_columns(
    pl.col("s").str.split(by="_").alias("split"))

# Remove leading and trailing characters
df.with_columns(foo_stripped=pl.col("foo").str.strip_chars())

# Count characters in all strings in a column
df.with_columns(
    pl.col("a").str.len_chars().alias("n_chars"))

# Check if string contains a substring that matches a pattern and doesn't use regex
df.select(pl.col("txt").str.contains("rab$", literal=True).alias("literal"))

# determines if any of the patterns find a match
df = pl.DataFrame(
    {
        "lyrics": [
            "Everybody wants to rule the world",
            "Tell me what you want, what you really really want",
            "Can you feel the love tonight",
        ]
    }
)
df.with_columns(
    pl.col("lyrics").str.contains_any(["you", "me"]).alias("contains_any")
)

# Return the index position of the first substring matching a pattern.
df.select(
    pl.col("txt"),
    pl.col("txt").str.find("a|e").alias("a|e (regex)"),
    pl.col("txt").str.find("e", literal=True).alias("e (lit)"),
)

# Drop duplicate rows
df_no_duplicates = df_with_duplicates.unique()

```
## Numerical Filters and queries 

```
# Iterate over the groups of the group by operation
for name, data in df.group_by(["foo"]):
    print(name)
    print(data)

# Basic group by functions
    # calculate total and average sales for each store
    df_pl.group_by(["store_code"]).agg(
        pl.sum("sales_qty").alias("total_sales"),
        pl.mean("sales_qty").alias("avg_sales")
    )

    # calculate total and average sales for each store-year pair
    df_pl.group_by(["store_code", "year"]).agg(
        pl.sum("sales_qty").alias("total_sales"),
        pl.mean("sales_qty").alias("avg_sales")
    )

    # create product lifetime and unique day count for each product
    df_pl.group_by(["product_code"]).agg(
        [
            pl.n_unique("sales_date").alias("unique_day_count"),
            ((pl.max("sales_date") - pl.min("sales_date")).dt.total_days() + 1).alias("lifetime")
        ]
    )

# Compute aggregations for each group of a group by operation
df.group_by("a").agg(pl.col("b"), pl.col("c"))

# Compute multiple aggregates at once by passing a list of expressions
df.group_by("a").agg([pl.sum("b"), pl.mean("c")])

# Compute the sum of a column for each group
df.group_by("a").agg(pl.col("b").sum())

# Filter on multiple conditions
df.filter((pl.col("foo") < 3) & (pl.col("ham") == "a"))

# Create a spreadsheet-style pivot table as a DataFrame
df.pivot(index="foo", columns="bar", values="baz", aggregate_function="sum")

# Pivot using selectors to determine the index/values/columns
df.pivot(
    index=cs.string(),
    columns=cs.string(),
    values=cs.numeric(),
    aggregate_function="sum",
    sort_columns=True,
).sort(
    by=cs.string(),
)

# Select columns from df
df.select(["foo", "bar"])

# Start a when-then-otherwise expression
df.with_columns(pl.when(pl.col("foo") > 2).then(1).otherwise(-1).alias("val"))

# Window function for grouping by single column
df.with_columns(
    pl.col("c").max().over("a").name.suffix("_max"),
)

# Window function for grouping by multiple columns by passing a list of column names or expressions
df.with_columns(
    pl.col("c").min().over(["a", "b"]).name.suffix("_min"),
)
```

## Lambda functions

```

df.with_column(pl.col('A').apply(lambda x: x*2))

```