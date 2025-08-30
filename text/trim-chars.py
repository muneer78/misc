import pandas as pd


def whitespace_remover(dataframe):
    # iterating over the columns
    for i in dataframe.columns:
        # checking datatype of each columns
        if dataframe[i].dtype == "object":
            # applying strip function on column
            dataframe[i] = dataframe[i].astype(str).map(str.strip)
        else:
            # if condn. is False then it will do nothing.
            pass


# Read the CSV files into DataFrames with error handling
df1 = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\order_post_hist-20241210-LME.csv",
    on_bad_lines="warn",
)
df2 = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\order_post_hist-20241210-Aurora_Prod.csv",
    on_bad_lines="warn",
)

dfs = [df1, df2]
output_files = [
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\order_post_hist-20241210-LMEv2.csv",
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\order_post_hist-20241210-Aurora_Prodv2.csv",
]

# Process each DataFrame and write to the respective CSV file
for df, output_file in zip(dfs, output_files):
    whitespace_remover(df)
    df.to_csv(output_file, index=False)

print("Done")
