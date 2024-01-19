import pandas as pd
def preprocessing(athlete_df,regions_df):
    athlete_df = athlete_df[athlete_df['Season'] == 'Summer']
    athlete_df = athlete_df.merge(regions_df, on='NOC', how='left')
    athlete_df.drop_duplicates(inplace=True)
    athlete_df = pd.concat([athlete_df, pd.get_dummies(athlete_df['Medal'])], axis=1)

    return athlete_df