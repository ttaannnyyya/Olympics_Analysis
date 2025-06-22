import streamlit as st
import pandas as pd
import helper
import preprocessor
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from helper import medal_tally

url = "https://drive.google.com/uc?export=download&id=1CObcF0i76VssLcgA7gsrifFzjtnXMB1H"

df = pd.read_csv(url)
region_df = pd.read_csv('noc_regions.csv')
df=preprocessor.preprocessor(df,region_df)

st.sidebar.title('Olympics Analysis ')
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/4/40/Olympics_logo.png", width=150)

User_Menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis', 'Country-wise Analysis','Athlete-wise Analysis')
)

# st.dataframe(df)

if User_Menu=='Medal Tally':

    st.sidebar.header('Medal Tally')
    years, country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally')
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f'Medal Tally for {selected_country} (All Years)')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'Medal Tally in {selected_year} (All Countries)')
    else:
        st.title(f'Medal Tally for {selected_country} in {selected_year}')

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    st.table(medal_tally)

if User_Menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1  # minus 1 if you have 'Overall'
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]  # FIXED typo here!

    st.title('Top Statistics')
    # 1st row: Editions, Hosts, Sports
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    # 2nd row: Events, Nations, Athletes
    col4, col5, col6 = st.columns(3)
    with col4:
        st.header('Events')
        st.title(events)
    with col5:
        st.header('Nations')
        st.title(nations)
    with col6:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time=helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title('Participating Nations over the Years')
    st.plotly_chart(fig)

    Events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(Events_over_time, x="Edition", y='Event')
    st.title('Events over the Years')
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y='Name')
    st.title('Athletes over the Years')
    st.plotly_chart(fig)

    st.title('Number of events over time(Every Sport)')
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title('Most successful Athletes')
    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')
    selected_sport = st.selectbox('Select Sport', sport_list)
    x = helper.mostsuccessful(df, selected_sport)

    st.table(x)

if User_Menu == 'Country-wise Analysis':
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    country_names = temp_df['region'].dropna().unique().tolist()  # <-- FIXED
    country_names.sort()
    country_names.insert(0, 'overall')
    st.title('Country-wise Medal Tally over Years')
    selected_country = st.selectbox('Select Country', country_names)

    bf = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(bf, x="Year", y="Medal")

    st.plotly_chart(fig)

if User_Menu == 'Athlete-wise Analysis':

    #Use ALL rows for medal-specific groups
    athlete_df = df.dropna(subset=['Age'])

    x1 = athlete_df.drop_duplicates(subset=['Name', 'region'])['Age']  # unique athletes' age
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age']
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age']
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age']

    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        show_hist=False,
        show_rug=False
    )
    fig.update_layout(autosize=False,width=1000,height=600)

    st.title("Distribution of Athlete Ages")
    st.plotly_chart(fig)
    # Create lists to store age data and sport names
    x = []
    name = []

    # List of sports to include
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
        'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions',
        'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
        'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling',
        'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery',
        'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball',
        'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
    ]

    # Loop through each sport and collect ages of gold medalists
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    # Create the distplot
    figg = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    figg.update_layout(autosize=False, width=1000, height=600)

    # Display the plot
    st.title("Distribution of Age w.r.t Sports(Gold Medalist)")
    st.plotly_chart(figg)

    sport_options = famous_sports
    sport_options.sort()
    sport_options.insert(0, 'overall')
    st.title('Weight vs Height Analysis')
    selected_sport = st.selectbox('Select Sport', sport_options)

    # Filter data
    temp_df = helper.weight_v_height(df, selected_sport)

    # Create a Matplotlib figure

    fig, ax = plt.subplots(figsize=(8, 8))
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', ax=ax)

    # Show it in Streamlit
    st.pyplot(fig)


    final = helper.men_vs_women_participation(df)

    # 📌 Create line plot
    fig = px.line(final, x="Year", y=["Male", "Female"],
                  labels={"value": "Number of Athletes", "variable": "Gender"},
                  title="Participation of Men and Women Over the Years")

    # 📌 Show in Streamlit
    st.title("Men vs Women Participation Over the Years")
    st.plotly_chart(fig)












