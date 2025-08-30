import polars as pl
import pandas as pd
from rich import print

# Generate the range of values from 4000 to 8000, stepped by 100
values = list(range(4000, 8001, 100))

df = pl.DataFrame({
    "MilesDriven" :values
})

# Calculate offset
purchase_price = 20887
df = df.with_columns(
    (purchase_price * pl.col("MilesDriven") / 120000).round(2).alias("MileageOffset")
)

# Calculate settlement total
df = df.with_columns(
    (purchase_price - pl.col("MileageOffset")).cast(pl.Float64).round(2).alias("SettlementTotal")
)

# Format columns as currency
df = df.with_columns(
    pl.col("MileageOffset").apply(lambda x: f"${x:,.2f}").alias("MileageOffset"),
    pl.col("SettlementTotal").apply(lambda x: f"${x:,.2f}").alias("SettlementTotal")
)

# Export the DataFrame to a CSV file
df.write_csv("settlementamounts.csv")