import polars as pl

# DS4271

# Read CSV files into Polars DataFrames
df = pl.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\DS4702reload.csv")

# # Update all values from None to test
# updated_df = df.with_columns(pl.col("partner_entity_id__c").replace(None, "test"))

# updated_df.write_csv("DS4721filltest.csv")

updated_df = df.with_columns(pl.col("partner_entity_id__c").replace("test", ""))
filtered_df = updated_df.filter(~pl.col("partner_entity_id__c").is_null())

updated_df.write_csv("DS4721updateone.csv")

print("Done")
