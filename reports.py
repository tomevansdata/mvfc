import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from display import lineups, match_report, match_report_mobile, scorecard, scorecard_mobile
from sheets import get_data

st.set_page_config(layout="wide", page_title='MVFC: Match Reports', page_icon = 'images/clubs/merseyvalley.png')

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

### Match Selector ###
selected_match = st.selectbox("Select a Match", options=["All"] + sorted(filtered_df["Match_Desc"], reverse=True))

### Match Report
if selected_match and selected_match != "All":
    
    match_row = filtered_df[filtered_df["Match_Desc"] == selected_match].iloc[0]
    
    if mobile_site:
        scorecard_mobile(match_row=match_row, home=True)
        scorecard_mobile(match_row=match_row, home=False)
        match_report_mobile(match_row=match_row)
    else:
        scorecard(match_row=match_row, home=True)
        scorecard(match_row=match_row, home=False)
        match_report(match_row=match_row)


    if mobile_site is False:
        st.markdown(f"<br><br>", unsafe_allow_html=True)
    
    if match_row["Score"] != "A-A":
        lineups(match_row=match_row, mobile_site=mobile_site)