import numpy as np

def medal_tally(athlete_df):
    medal_tally = athlete_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']


    return medal_tally

def country_year(athlete_df):
    years = athlete_df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(athlete_df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def fetch_medal_tally(athlete_df,year,country):
    medal_df = athlete_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]

    if flag == 1:
        x = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
        x['Year'] = x['Year'].astype(str).str.replace(',', '')
    else:
        x = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def participating_nation_over_time(athlete_df):
    nation_over_time = athlete_df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    nation_over_time.rename(columns={'Year': 'Edition', 'count': 'No. of Countries'}, inplace=True)

    return nation_over_time

def events_over_time(athlete_df):
    event_over_time = athlete_df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year')
    event_over_time.rename(columns={'Year': 'Edition', 'count': 'No. of Events'}, inplace=True)

    return event_over_time

def athletes_over_time(athlete_df):
    athlete_over_time = athlete_df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('Year')
    athlete_over_time.rename(columns={'Year': 'Edition', 'count': 'No. of Athletes'}, inplace=True)

    return athlete_over_time


def most_successful(athlete_df, sport):
    temp_df = athlete_df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(athlete_df, how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')

    x.rename(columns={'count': 'Medals'}, inplace=True)

    return x


def year_wise_medal(athlete_df, country):
    temp_df = athlete_df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    f_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return f_df

def country_wise_heatmap(athlete_df, country):
    temp_df = athlete_df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index = 'Sport',columns= "Year",values = 'Medal',aggfunc='count').fillna(0).astype('int')

    return pt

def most_successful_countrywise(athlete_df, country):
    temp_df = athlete_df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(athlete_df, how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')

    x.rename(columns={'count': 'Medals'}, inplace=True)

    return x

def weight_height(athlete_df,sport):
    a_df = athlete_df.drop_duplicates(subset=['Name', 'region'])
    a_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = a_df[a_df['Sport'] == sport]
        return temp_df
    else:
        return a_df


def men_vs_women(athlete_df):
    a_df = athlete_df.drop_duplicates(subset=['Name', 'region'])
    men = a_df[a_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = a_df[a_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final

