import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from sheets import get_data

st.set_page_config(layout="wide", page_title='MVFC: Team Stats', page_icon = 'images/clubs/merseyvalley.png')

### Get Data ###
df = get_data("MatchData")

screen_width = streamlit_js_eval(js_expressions='screen.width', key = 'SCR')
mobile_site = False
max_width = 800

if screen_width is not None and screen_width < 650:
    mobile_site = True
    max_width = screen_width

### Set container width
st.markdown(f"""
    <style>
    .block-container {{
        max-width: {max_width}px;
        margin: auto;
    }}
    </style>
    """, unsafe_allow_html=True)

### Header ###
st.image("images/misc/mersey_valley_football_club_cover.jpeg")

### Filters ###
month_year_combinations = sorted(df['month_year'].unique(), key=lambda x: pd.to_datetime(x))

age_group = st.selectbox("Select Age Group:", options=["All"] + list(df["AgeGroup"].unique()))
team_name = st.selectbox("Select Team :", options=["All"] + list(df["Team"].unique()))
competition = st.selectbox("Select Competition:", options=["All"] + list(df["Competition"].unique()))
selected_date = st.selectbox("Select Date:", options=["All"] + month_year_combinations)

filtered_df = df.copy()
if age_group != "All":
    filtered_df = filtered_df[filtered_df["AgeGroup"] == age_group]
if team_name != "All":
    filtered_df = filtered_df[filtered_df["Team"] == team_name]
if competition != "All":
    filtered_df = filtered_df[filtered_df["Competition"] == competition]
if selected_date != "All":
    filtered_df = filtered_df[filtered_df["month_year"] == selected_date]


filtered_df = filtered_df[filtered_df["Score"] != "A-A"]
filtered_df = filtered_df.rename(columns={
    "won": "W",
    "drew": "D",
    "lost": "L",
    "unknown": "U",
    "goals_for": "GF",
    "goals_against": "GA",
    })
filtered_df["Played"] = 1

team_df = filtered_df[['Team', 'Played', 'W', 'D', 'L', 'U', 'GF', 'GA']].groupby('Team').sum()
total_row = pd.DataFrame(team_df.sum(axis=0)).T
total_row.index = ['Total']

team_df = pd.concat([team_df, total_row])
team_df["GD"] = team_df["GF"] - team_df["GA"]

st.markdown(f"<br><br>", unsafe_allow_html=True)
st.dataframe(team_df, use_container_width=True)
