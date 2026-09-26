import polars as pl

df = pl.read_excel(
    source=r"C:\Users\mahmad\OneDrive - Ryan RTS\1- Projects\datasets needing lineage .xlsx",
    sheet_name="Sheet1",
)

df_select = df.select(["workspace id", "dataset id", "Github Ref", "dataset name"])
# Add new columns with the new headers
df_final = df_select.with_columns(
    [
        pl.Series("db_type", [None] * df.height),
        pl.Series("db_name", [None] * df.height),
        pl.Series("schema_name", [None] * df.height),
        pl.Series("tables_name", [None] * df.height),
    ]
)

df_renamed = df_final.rename(
    {
        "workspace id": "workspace_id",
        "dataset id": "dataset_id",
        "Github Ref": "pbi_workspace_name",
        "dataset name": "dataset_name",
    }
)

df_renamed.write_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\1- Projects\DS5121.csv")
