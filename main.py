import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from streamlit_extras.stylable_container import stylable_container

from display import lineups, match_report, scorecard
from sheets import get_sheet_data

st.set_page_config(layout="wide")

#st.write(f"Screen width is {(streamlit_js_eval(js_expressions='screen.width', key = 'SCR'))}")

### Get Data ###
df = get_sheet_data("MatchData")

st.markdown("""
    <style>
    .block-container {
        max-width: 800px;
        margin: auto;
    }
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

### Match Selector ###
selected_match = st.selectbox("Select a Match", options=["All"] + sorted(filtered_df["Match_Desc"], reverse=True))

### Match Report
if selected_match and selected_match != "All":
    
    match_row = filtered_df[filtered_df["Match_Desc"] == selected_match].iloc[0]
    
    scorecard(match_row=match_row, home=True)
    scorecard(match_row=match_row, home=False)
    
    match_report(match_row=match_row)
    
    st.markdown(f"<br><br>", unsafe_allow_html=True)
    
    lineups(match_row=match_row)
