import petl as etl

# Read a CSV file into a Petl table
table = etl.fromcsv("data.csv")

# Filter rows based on a condition
filtered_table = etl.select(table, lambda rec: rec["age"] > 30)

# Perform a join operation
joined_table = etl.join(table1, table2, key="user_id")

# Perform aggregation
aggregated_table = etl.aggregate(
    table, key="category", aggregation={"count": etl.Count()}
)

# Write the table to a new CSV file
etl.tocsv(aggregated_table, "output.csv")
