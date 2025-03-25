'''
1. Make sure excluded.csv is in same folder as script
	- Need to update this file at the beginning of each season
2. Download the following reports from Fangraphs
	- 10 IP Pitchers
	- 30 IP Pitchers
	- 40 PA Hitters
	- Hitters Last 14 Days
	- Hitters Last 7 Days
	- Pitchers Last 14 Days
	- Pitchers Last 30 Days
	- ZScoreHitter
	- ZScorePitcher
3. Download chart for average game score: https://www.baseball-reference.com/leagues/majors/2023-starter-pitching.shtml
'''

import pandas as pd
from datetime import date, datetime
import os
from scipy import stats

# define dictionary
comp_dict = {
    "fangraphs-leaderboards.csv": "fgl_pitchers_10_ip.csv",
    "fangraphs-leaderboards (1).csv": "fgl_pitchers_30_ip.csv",
    "fangraphs-leaderboards (2).csv": "fgl_hitters_40_pa.csv",
    "fangraphs-leaderboards (3).csv": "fgl_hitters_last_14.csv",
    "fangraphs-leaderboards (4).csv": "fgl_hitters_last_7.csv",
    "fangraphs-leaderboards (5).csv": "fgl_pitchers_last_14.csv",
    "fangraphs-leaderboards (6).csv": "fgl_pitchers_last_30.csv",
    "fangraphs-leaderboards (7).csv": "hitter.csv",
    "fangraphs-leaderboards (8).csv": "pitcher.csv",
}

for newname, oldname in comp_dict.items():
    os.replace(newname, oldname)

excluded = pd.read_csv("excluded.csv")

def process_and_merge_data(data_df, temp_data, id_columns, numeric_columns, zscore_columns):
    df = data_df.copy()
    temp_df = temp_data[['Name', 'PlayerId']]

    df = df.drop(columns=id_columns)
    df = df.fillna(0)

    df[numeric_columns] = df[numeric_columns].astype('float')

    numbers = df.select_dtypes(include='number').columns
    df[numbers] = df[numbers].apply(stats.zscore)

    df['Total Z-Score'] = df[numbers].sum(axis=1).round(2)

    df = df.merge(temp_df[['Name', 'PlayerId']], on=["Name"], how="left")

    return df


# Load the data
dfhitter = pd.read_csv('hitter.csv')
dfpitcher = pd.read_csv('pitcher.csv')

# Define columns for processing hitters and pitchers
hitter_id_columns = ['PlayerId', 'MLBAMID']
hitter_numeric_columns = ["PA", "HR", "SB", 'BABIP+', 'K%+', 'BB%+', 'ISO+', 'wRC+', 'Barrels', "Barrel%"]
hitter_zscore_columns = hitter_numeric_columns + ['Total Z-Score']

pitcher_id_columns = ['PlayerId', 'MLBAMID']
pitcher_numeric_columns = ['Stuff+', 'Location+', 'Pitching+', 'Starting', 'Relieving']
pitcher_zscore_columns = pitcher_numeric_columns + ['Total Z-Score']

# Process hitter and pitcher data
dfhitter_processed = process_and_merge_data(dfhitter, dfhitter, hitter_id_columns, hitter_numeric_columns, hitter_zscore_columns)
dfpitcher_processed = process_and_merge_data(dfpitcher, dfpitcher, pitcher_id_columns, pitcher_numeric_columns, pitcher_zscore_columns)

# Add Total Z-Score column to the original DataFrames
dfhitter['Total Z-Score'] = dfhitter_processed['Total Z-Score']
dfpitcher['Total Z-Score'] = dfpitcher_processed['Total Z-Score']

today = date.today()
today = datetime.strptime(
    "2024-10-31", "%Y-%m-%d"
).date()  # pinning to last day of baseball season

def hitters_wk_preprocessing(filepath):
    '''Creates weekly hitter calcs'''
    df = pd.read_csv(filepath, index_col=["PlayerId"])

    filter = df[(df["PA"] > 10)]

    df.columns = df.columns.str.replace("[+,-,%,]", "", regex=True)
    df.rename(columns={"K%-": "K", "BB%-": "BB"}, inplace=True)
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["PlayerId"].isin(excluded["PlayerId"])]
    df = df.merge(dfhitter[["PlayerId", "Total Z-Score"]], on=["PlayerId"], how="left")

    filters = df[
        (df["wRC"] > 115)
        & (df["OPS"] > 0.8)
        & (df["K"] < 100)
        & (df["BB"] > 100)
        & (df["Off"] > 3)
        # & (df["Barrel"] > 5)
    ].sort_values(by="Off", ascending=False)
    return filters


def hitters_pa_preprocessing(filepath):
    df = pd.read_csv(filepath, index_col=["PlayerId"])

    filter = df[(df["PA"] > 10)]

    df.columns = df.columns.str.replace("[+,-,%,]", "", regex=True)
    df.rename(columns={"K%-": "K", "BB%-": "BB"}, inplace=True)
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["PlayerId"].isin(excluded["PlayerId"])]
    df = df.merge(dfhitter[["PlayerId", "Total Z-Score"]], on=["PlayerId"], how="left")

    filters = df[
        (df["wRC"] > 115)
        & (df["OPS"] > 0.8)
        & (df["K"] < 110)
        & (df["BB"] > 90)
        & (df["Off"] > 3)
        # & (df["Barrel"] > 5)
        & (df["PA"] > 40)
    ].sort_values(by="Off", ascending=False)
    return filters


def sp_preprocessing(filepath):
    df = pd.read_csv(filepath, index_col=["PlayerId"])

    df.columns = df.columns.str.replace("[+,-,%,]", "", regex=True)
    df.rename(
        columns={"K/BB": "KToBB", "HR/9": "HRPer9", "xFIP-": "XFIPMinus"}, inplace=True
    )
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["PlayerId"].isin(excluded["PlayerId"])]
    df = df.merge(dfpitcher[["PlayerId", "Total Z-Score"]], on=["PlayerId"], how="left")

    filters1 = df[
        (df["Barrel"] < 7)
        & (df["Starting"] > 5)
        & (df["GS"] > 1)
        & (df["Pitching"] > 99)
        & (df["Total Z-Score"] > 8)
    ].sort_values(by="Starting", ascending=False)
    return filters1


def rp_preprocessing(filepath):
    df = pd.read_csv(filepath, index_col=["PlayerId"])

    df.columns = df.columns.str.replace("[+,-,%,]", "", regex=True)
    df.rename(
        columns={"K/BB": "KToBB", "HR/9": "HRPer9", "xFIP-": "XFIPMinus"}, inplace=True
    )
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["PlayerId"].isin(excluded["PlayerId"])]
    df = df.merge(dfpitcher[["PlayerId", "Total Z-Score"]], on=["PlayerId"], how="left")

    filters2 = df[
        (df["Barrel"] < 7)
        & (df["Total Z-Score"] > 8)
        & (df["Relieving"] > 0)
        & (df["Pitching"] > 99)
    ].sort_values(by="Relieving", ascending=False)
    return filters2


# Preprocess and export the dataframes to Excel workbook sheets
hitdaywindow = [7, 14]
pawindow = [40]
pitchdaywindow = [14, 30]
ipwindow = [10, 30]

df_list = []

# Initialize a list to keep track of printed titles
printed_titles = []

with open("weeklyadds.csv", "w+") as f:
    for w in hitdaywindow:
        df = hitters_wk_preprocessing(f"fgl_hitters_last_{w}.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"Hitters Last {w} Days"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

    for w in pawindow:
        df = hitters_pa_preprocessing(f"fgl_hitters_{w}_pa.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"Hitters {w} PA"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

    for w in ipwindow:
        df = sp_preprocessing(f"fgl_pitchers_{w}_ip.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"SP {w} Innings"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

        df = rp_preprocessing(f"fgl_pitchers_{w}_ip.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"RP {w} Innings"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

    for w in pitchdaywindow:
        df = sp_preprocessing(f"fgl_pitchers_last_{w}.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"Pitchers Last {w} Days"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)

        df = rp_preprocessing(f"fgl_pitchers_last_{w}.csv")
        df = df.sort_values(by="Total Z-Score", ascending=False)
        df_list.append(df)
        title = f"RP Last {w} Days"
        if not df.empty and title not in printed_titles:
            f.write(f"{title}\n")
            df.round(2).to_csv(f, index=False)
            f.write("\n")
            printed_titles.append(title)
print('All done')