# PySpark code snippets

## EDA

```
# loading file
df = spark.read.load("/home/rahul/projects/sparkdf/coronavirusdataset/Case.csv",format="csv", sep=",", inferSchema="true", header="true")

# provides a detailed, verbose output of the query plan
df.explain(true)

# read JSON
dataframe = sc.read.json('dataset/nyt2.json')

# read txt 
dataframe_txt = sc.read.text('text_data.txt')

# read csv 
dataframe_csv = sc.read.csv('csv_data.csv')

# read Parquet 
dataframe_parquet = sc.read.load('parquet_data.parquet')

# see a few rows
df.show()

# convert to pandas df
cases.limit(10).toPandas()

# Returns dataframe column names and data types
dataframe.dtypes

# Displays the content of dataframe
dataframe.show()

# Return first n rows
dataframe.head()

# Returns first row
dataframe.first()

# Return first n rows
dataframe.take(5)

# Computes summary statistics
dataframe.describe().show()

# Find number of unique values in a column
df.select('species').distinct().count()

# Returns columns of dataframe
dataframe.columns

# Counts the number of rows in dataframe
dataframe.count()

# Counts the number of distinct rows in dataframe
dataframe.distinct().count()

# Prints plans including physical and logical
dataframe.explain(4)

# Write & Save File in .parquet format
dataframe.select("author", "title", "rank", "description") \
.write \
.save("Rankings_Descriptions.parquet")

# Write & Save File in .json format
dataframe.select("author", "title") \
.write \
.save("Authors_Titles.json",format="json")

```

## Update dataset

```

# Combining two DataFrames
combined_df = df1.union(df2)

# change single column name
cases = cases.withColumnRenamed("infection_case","infection_source")

# change all columns names
cases = cases.toDF(*['case_id', 'province', 'city', 'group', 'infection_case', 'confirmed',
       'latitude', 'longitude'])

# choose columns for output
cases = cases.select('province','city','infection_case','confirmed')
cases.show()

# drop columns
dataframe_remove = dataframe.drop("publisher", "published_date").show(5)
dataframe_remove2 = dataframe \ .drop(dataframe.publisher).drop(dataframe.published_date).show(5)

# ascending sort
cases.sort("confirmed").show()

# descending sort
from pyspark.sql import functions as F
cases.sort(F.desc("confirmed")).show()

# sort by multiple columns
df.orderBy(['mass', 'flipper'], ascending=False).show(5)

# sort by multiple columns, but different on ascending and descending for each col
df[df['mass'].isNotNull()]\
  .sort('mass', 'flipper', ascending=[True, False]).show(5)

# convert data types
from pyspark.sql.types import DoubleType, IntegerType, StringType
cases = cases.withColumn('confirmed', F.col('confirmed').cast(IntegerType()))
cases = cases.withColumn('city', F.col('city').cast(StringType()))

# rename new column names after performing functions
cases.groupBy(["province","city"]).agg(
    F.sum("confirmed").alias("TotalConfirmed"),\
    F.max("confirmed").alias("MaxFromOneConfirmedCase")\
    ).show()

# create new column where you add 100 to another column's value
import pyspark.sql.functions as F
casesWithNewConfirmed = cases.withColumn("NewConfirmed", 100 + F.col("confirmed"))

# drop dupes
dataframe_dropdup = dataframe.dropDuplicates() 

# Replacing null values
dataframe.na.fill()
dataFrame.fillna()
dataFrameNaFunctions.fill()

# Returning new dataframe restricting rows with null valuesdataframe.na.drop()
dataFrame.dropna()
dataFrameNaFunctions.drop()

# Return new dataframe replacing one value with another
dataframe.na.replace(5, 15)
dataFrame.replace()
dataFrameNaFunctions.replace()

# capitalizes the first letter of each word in a string column
spark.createDataFrame([('ab cd',)], ['a']).select(initcap("a").alias('v')).collect()
[Row(v='Ab Cd')]

# percentile
df.groupBy("key").agg(percentile("value", 0.5, lit(1)).alias("median"))

# combine strings in df
df.withColumn("concat",F.concat("col1","col2")).show()

# do different aggregations on multiple columns
df.groupBy('species').agg({'flipper': 'sum', 'mass': 'mean'}).show()

```

## Categorical Filters and queries 

```
# filter df

from pyspark.sql import functions as F
cases.groupBy(["province","city"]).agg(F.sum("confirmed") ,F.max("confirmed")).show()

# Select when
dataframe.select("title",when(dataframe.title != 'ODD HOURS', 
1).otherwise(0)).show(10)

# is in
dataframe [dataframe.author.isin("John Sandford", 
"Emily Giffin")].show(5)

# filter partial string matches
dataframe.select("author", "title",
dataframe.title.like("% THE %")).show(15)

# filter starts with
dataframe.select("author", "title", dataframe.title.startswith("THE")).show(5)

# filter ends with
dataframe.select("author", "title", dataframe.title.endswith("NT")).show(5)

# substrings
dataframe.select(dataframe.author.substr(1, 3).alias("title")).show(5)
dataframe.select(dataframe.author.substr(3, 6).alias("title")).show(5)
dataframe.select(dataframe.author.substr(1, 6).alias("title")).show(5)

# regexp extract
# extract regex and split function
df = df.withColumn("Email_Service_Provider", regexp_extract("Email_ID", "@(.*?)\.", 1))

```
## Numerical Filters and queries 

```

# groupby
dataframe.groupBy("author").count().show(10)

# group the data by the "city" column and compute the average, sum, and count of the temperature for each city
grouped_df = df.groupBy("city").agg(avg("temperature").alias("avg_temperature"),
                                     sum("temperature").alias("total_temperature"),
                                     count("temperature").alias("num_measurements"))

# inner join
cases = cases.join(regions, ['province','city'],how='left')

# left join
left_join_result = df1.join(df2, "Name", "left")

# right join
right_join_result = df1.join(df2, "Name", "right")

# full outer join
full_outer_join_result = df1.join(df2, "Name", "outer")

# cross join
cross_join_result = df1.crossJoin(df2)

# joining on multiple columns
multi_col_join_result = df2.join(df3, "Designation", "left")

# coalesce
coalesced_df = df.withColumn("result", F.coalesce("col1", "col2", "col3"))

# broadcast small table when doing a join
from pyspark.sql.functions import broadcast
cases = cases.join(broadcast(regions), ['province','city'],how='left')

# window function
windowSpec = Window().partitionBy(['province']).orderBy(F.desc('confirmed'))
cases.withColumn("rank",F.rank().over(windowSpec)).show()

# lag variables
from pyspark.sql.window import Window
windowSpec = Window().partitionBy(['province']).orderBy('date')
timeprovinceWithLag = timeprovince.withColumn("lag_7",F.lag("confirmed", 7).over(windowSpec))
timeprovinceWithLag.filter(timeprovinceWithLag.date>'2020-03-10').show()

# rolling aggregations
from pyspark.sql.window import Window
windowSpec = Window().partitionBy(['province']).orderBy('date').rowsBetween(Window.unboundedPreceding,Window.currentRow)
timeprovinceWithRoll = timeprovince.withColumn("cumulative_confirmed",F.sum("confirmed").over(windowSpec))
timeprovinceWithRoll.filter(timeprovinceWithLag.date>'2020-03-10').show()

# 1. ROW_NUMBER() function
df_row_number = df.withColumn("row_num", row_number().over(window_spec))

# 2. RANK() function
df_rank = df.withColumn("rank", rank().over(window_spec))

# 3. DENSE_RANK() function
df_dense_rank = df.withColumn("dense_rank", dense_rank().over(window_spec))

# 4. LEAD() function - Shows the marks of the next student
df_lead = df.withColumn("lead_marks", lead("marks", 1).over(window_spec))

# 5. LAG() function - Shows the marks of the previous student
df_lag = df.withColumn("lag_marks", lag("marks", 1).over(window_spec))

# 6. Partitioning by multiple columns (e.g., 'id' and 'city') and using ROW_NUMBER()
window_multi = Window.partitionBy("id", "city").orderBy("marks")
df_multi_partition = df.withColumn("row_num_multi", row_number().over(window_multi))

# pivot
pivotedTimeprovince = timeprovince.groupBy('date').pivot('province').agg(F.sum('confirmed').alias('confirmed') , F.sum('released').alias('released'))
pivotedTimeprovince.limit(10).toPandas()

# unpivot
unpivotedTimeprovince = pivotedTimeprovince.select('date',F.expr(exprs))

```

## SQL
```

# run basic select statement
cases.registerTempTable('cases_table')
newDF = sqlContext.sql('select * from cases_table where confirmed>100')

```

## UDF
```

# create a UDF
import pyspark.sql.functions as F
from pyspark.sql.types import *
def casesHighLow(confirmed):
    if confirmed < 50: 
        return 'low'
    else:
        return 'high'
    
#convert to a UDF Function by passing in the function and return type of function
casesHighLowUDF = F.udf(casesHighLow, StringType())
CasesWithHighLow = cases.withColumn("HighLow", casesHighLowUDF("confirmed"))
CasesWithHighLow.show()

```