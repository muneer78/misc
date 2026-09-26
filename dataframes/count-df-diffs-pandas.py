import pandas as pd

# DS4220


def df_diff(
    df_A: pd.DataFrame, df_B: pd.DataFrame, on_A: str = "", on_B: str = ""
) -> pd.DataFrame:
    """
    Function: Compare DataFrame "A" and "B" to find rows only in "A" but not in "B"

    Input:
        df_A: DataFrame "A" ("left table")
        df_B: DataFrame "B" ("right table")
        on_A: column name in DataFrame "A" to compare on. If not provided/valid, will default to using df_A's index
        on_B: column name in DataFrame "B" to compare on. If not provided/valid, will default to using df_B's index

    Output:
        DataFrame containing diff result (all rows only in df_A but not in df_B, and same columns as df_A)
        If find zero rows, will return a DataFrame of 0 row and same columns as df_A (can be checked by `df_output.empty and df_output.shape[1] != 0`)
        If input is not valid DataFrame, will return a DataFrame of 0 row and 0 column (can be checked by `df_output.empty and df_output.shape[1] == 0`)

    Dependency: `import pandas as pd`

    History: 2022-02-07 Developed by frank-yifei-wang@GitHub
    """

    if type(df_A) != pd.core.frame.DataFrame or type(df_B) != pd.core.frame.DataFrame:
        return pd.DataFrame()

    if on_A != "" and on_A in df_A.columns:
        id_col_A = df_A[on_A]
    else:
        id_col_A = df_A.index
    if on_B != "" and on_B in df_B.columns:
        id_col_B = df_B[on_B]
    else:
        id_col_B = df_B.index

    id_set_A = set(id_col_A)
    id_set_B = set(id_col_B)

    id_set_diff = id_set_A.difference(id_set_B)
    df_output = df_A[id_col_A.isin(id_set_diff)].copy()

    return df_output


def df_overlap(
    df_A: pd.DataFrame, df_B: pd.DataFrame, on_A: str = "", on_B: str = ""
) -> pd.DataFrame:
    """
    Function: Compare DataFrame "A" and "B" to find rows in "A" and also in "B"

    Input:
        df_A: DataFrame "A" ("left table")
        df_B: DataFrame "B" ("right table")
        on_A: column name in DataFrame "A" to compare on. If not provided/valid, will default to using df_A's index
        on_B: column name in DataFrame "B" to compare on. If not provided/valid, will default to using df_B's index

    Output:
        DataFrame containing overlap result (all rows in df_A and also in df_B, and same columns as df_A)
        Note: result of df_overlap(df_A, df_B) (= a slice of df_A) is different from df_overlap(df_B, df_A) (= a slice of df_B)
        If find zero rows, will return a DataFrame of 0 row and same columns as df_A (can be checked by `df_output.empty and df_output.shape[1] != 0`)
        If input is not valid DataFrame, will return a DataFrame of 0 row and 0 column (can be checked by `df_output.empty and df_output.shape[1] == 0`)

    Dependency: `import pandas as pd`

    History: 2022-02-07 Developed by frank-yifei-wang@GitHub
    """

    if type(df_A) != pd.core.frame.DataFrame or type(df_B) != pd.core.frame.DataFrame:
        return pd.DataFrame()

    if on_A != "" and on_A in df_A.columns:
        id_col_A = df_A[on_A]
    else:
        id_col_A = df_A.index
    if on_B != "" and on_B in df_B.columns:
        id_col_B = df_B[on_B]
    else:
        id_col_B = df_B.index

    id_set_A = set(id_col_A)
    id_set_B = set(id_col_B)

    id_set_overlap = id_set_A.intersection(id_set_B)
    df_output = df_A[id_col_A.isin(id_set_overlap)].copy()

    return df_output


df_A_csv = pd.read_csv("DS4220-20240517.csv")
df_B_csv = pd.read_csv("TransactionSummaryLLCGrp_Daily_184835_05-09-2024v2.csv")

id_col1 = "transid"
id_col2 = "Trans. Id"
# id_col = ""  # Test id omission

df_A_only = df_diff(df_A_csv, df_B_csv, on_A=id_col1, on_B=id_col2)
df_A_only["Rownum_In_Original"] = df_A_only.index + 2
df_A_only.to_csv("A_only.csv", index=False)

df_B_only = df_diff(df_B_csv, df_A_csv, on_A=id_col1, on_B=id_col2)
df_B_only["Rownum_In_Original"] = df_B_only.index + 2
df_B_only.to_csv("B_only.csv", index=False)

df_A_B_both = df_overlap(df_A_csv, df_B_csv, on_A=id_col1, on_B=id_col2)
df_A_B_both["Rownum_In_Original"] = df_A_B_both.index + 2
df_A_B_both.to_csv("A_B_both.csv", index=False)

df_B_A_both = df_overlap(df_B_csv, df_A_csv, on_A=id_col1, on_B=id_col2)
df_B_A_both["Rownum_In_Original"] = df_B_A_both.index + 2
