import polars as pl

df = pl.read_csv(r"/Users/muneer78/Downloads/vinyl.csv")

print(df.columns)

df_rename = df.rename({"name": "title"})

selected_df = df_rename.select("artist", "title", "album")

sorted_df = selected_df.sort(pl.col("artist").str.to_lowercase(), descending=False)

sorted_df.write_csv(r"/Users/muneer78/Downloads/vinyl-final.csv")
