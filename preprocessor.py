import pandas as pd



def preprocessor(df,region_df):
    # global df, region_df

    # ✅ 1) Use only needed columns from region_df
    region_df_clean = region_df[['NOC', 'region']].drop_duplicates()

    # ✅ 2) Filter for Summer Olympics
    df_summer = df[df['Season'] == 'Summer'].copy()

    # ✅ 3) Drop 'region' if already present in df_summer (important!)
    if 'region' in df_summer.columns:
        df_summer = df_summer.drop(columns=['region'])

    # ✅ 4) Merge safely
    df_summer = df_summer.merge(region_df_clean, on='NOC', how='left')

    # ✅ 5) Drop duplicates
    df_summer.drop_duplicates(inplace=True)

    # ✅ 6) One-hot encode 'Medal'
    df_summer = pd.concat([df_summer, pd.get_dummies(df_summer['Medal'])], axis=1)

    return df_summer
