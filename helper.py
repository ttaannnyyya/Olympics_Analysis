def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                             ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype(int)
    medal_tally['Silver']=medal_tally['Silver'].astype(int)
    medal_tally['Bronze']=medal_tally['Bronze'].astype(int)
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = df['region'].dropna().unique()
    country = country.tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    # Ensure consistent capitalization
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    # Ensure integers for medal counts
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def data_over_time(df,col):
    nations_over_time = (
        df.drop_duplicates(['Year', col])
        ['Year'].value_counts()
        .reset_index()
        .sort_values('Year')  # ✅ Correct!
        .rename(columns={'Year': 'Edition', 'count': col})
    )

    return nations_over_time

def mostsuccessful(df, sport):
    # Keep only rows with a medal
    temp_df = df.dropna(subset=['Medal'])

    # If a specific sport is chosen, filter
    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Get top 15 athletes by medal count
    top_athletes = (
        temp_df['Name'].value_counts()
        .reset_index(name='Medal Count')   # => first column auto-named 'Name'
        .head(15)
    )

    # Ensure columns are ['Name', 'Medal Count']
    top_athletes.columns = ['Name', 'Medal Count']

    # Merge to get sport & region info
    top_athletes = top_athletes.merge(
        df, on='Name', how='left'
    )[['Name', 'Medal Count', 'Sport', 'region']].drop_duplicates('Name')

    return top_athletes

def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    if country != 'overall':
        temp_df = temp_df[temp_df['region'] == country]

    final_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if(sport!='overall'):
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
        temp_df = athlete_df
    return temp_df




def men_vs_women_participation(df):
    """
    Computes year-wise count of male and female athletes.
    Returns a DataFrame with columns: Year, Male, Female.
    """
    athlete_df = df.drop_duplicates(subset=['Name', 'region', 'Year', 'Sport', 'Event'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final

