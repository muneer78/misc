import pandas as pd

bat_df = pd.read_csv('96bat.csv')
pitch_df = pd.read_csv('96pitch.csv')

print("Batting columns:", bat_df.columns)
print("Pitching columns:", pitch_df.columns)
print("Batting head:")
print(bat_df[['Player', 'Player-additional', 'WAR']].head())
print("Pitching head:")
print(pitch_df[['Player', 'Player-additional', 'WAR']].head())

# Check for duplicates in 'Player-additional'
print("Duplicates in bat:", bat_df['Player-additional'].duplicated().sum())
print("Duplicates in pitch:", pitch_df['Player-additional'].duplicated().sum())

# Preparing DataFrames
bat_df = bat_df.rename(columns={'WAR': 'WAR_Bat'})
pitch_df = pitch_df.rename(columns={'WAR': 'WAR_Pitch'})

# Drop 'Rk' as it's redundant/specific to the original file, or keep it?
# The user wants "combined csv". Let's drop Rk or rename it. I'll drop it.

# Merging
merged_df = pd.merge(bat_df, pitch_df, on=['Player-additional', 'Team'], how='outer', suffixes=('_Bat', '_Pitch'))

# Cleanup columns
# 'Age_Bat' and 'Age_Pitch' should be same, combine them
merged_df['Age'] = merged_df['Age_Bat'].combine_first(merged_df['Age_Pitch'])
merged_df['Lg'] = merged_df['Lg_Bat'].combine_first(merged_df['Lg_Pitch'])
merged_df['Player'] = merged_df['Player_Bat'].combine_first(merged_df['Player_Pitch'])

# Drop the x/y suffix columns if they are redundant
merged_df = merged_df.drop(columns=['Age_Bat', 'Age_Pitch', 'Lg_Bat', 'Lg_Pitch', 'Player_Bat', 'Player_Pitch', 'Rk_Bat', 'Rk_Pitch', 'Awards_Bat', 'Awards_Pitch'])

# Calculate Total WAR
merged_df['WAR_Bat'] = merged_df['WAR_Bat'].fillna(0)
merged_df['WAR_Pitch'] = merged_df['WAR_Pitch'].fillna(0)
merged_df['Total_WAR'] = merged_df['WAR_Bat'] + merged_df['WAR_Pitch']

# Sort
merged_df = merged_df.sort_values(by='Total_WAR', ascending=False)

# Save
merged_df.to_csv('combined_stats.csv', index=False)
print("Done. Saved to combined_stats.csv")
print(merged_df.head())

