import pandas as pd

# DS4220

try:
    df2 = pd.read_csv(
        "TransactionSummaryLLCGrp_Daily_184835_05-09-2024.csv", on_bad_lines="skip"
    )

    # Replace '|' with ',' in the entire DataFrame
    df2 = df2.map(lambda x: x.replace("|", ",") if isinstance(x, str) else x)

    # Replace '|' with ',' in the column names
    df2.columns = [
        col.replace("|", ",") if isinstance(col, str) else col for col in df2.columns
    ]

    # Save the cleaned DataFrame to a new CSV file
    df2.to_csv("TransactionSummaryLLCGrp_Daily_184835_05-09-2024v2.csv", index=False)

except pd.errors.ParserError as e:
    print(f"ParserError: {e}")
