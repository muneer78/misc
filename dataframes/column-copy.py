import polars as pl


def copy(input_csv, output_csv):
    df = pl.read_csv(input_csv)
    df = df.with_columns([pl.col("sf_region").alias("region")])
    df.write_csv(output_csv)


# Example usage:
copy_sf_region_to_region(
    "/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Downloads/sales_regions.csv",
    "/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Downloads/sales_regions-output.csv",
)
