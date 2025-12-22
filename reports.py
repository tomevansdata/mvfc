import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from display import scorecard
from functions import get_match_list, get_match_data, apply_filters
from style import match_report_mobile_style, pitch_style, scorecard_style, scorecard_mobile_style


st.set_page_config(layout="wide", page_title='MVFC: Match Reports', page_icon = 'images/clubs/merseyvalley.png')

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

query_params = st.query_params
match_id_nav = query_params.get("match_id", None)

### Get Data ###
df = get_match_list()

### Apply reusable filters
filtered_df, filters = apply_filters(df)

### Match Selector ###
selected_match = st.selectbox("Select a Match", options=["Please select..."] + sorted(filtered_df["match_header"], reverse=True))

### Match Report
if (selected_match and selected_match != "Please select...") or match_id_nav:
       
    if match_id_nav:
        st.write(match_id_nav)
        match_id = int(match_id_nav)
    else:
        match_select_row = filtered_df[filtered_df["match_header"] == selected_match].iloc[0]
        match_id = match_select_row['match_id']
    
    st.write(f"Selected Match ID: {match_id}")
    match_df = get_match_data(match_id)
    match_row = match_df.iloc[0]

    if match_row["mv_home_display"]:
        scorecard(match_row=match_row, mv=True)
        scorecard(match_row=match_row, mv=False)
    else:
        scorecard(match_row=match_row, mv=False)
        scorecard(match_row=match_row, mv=True)
        
    st.markdown(f"<br><br>", unsafe_allow_html=True)
    
    st.map({
        "lat": [match_row["lat"]],
        "lon": [match_row["lon"]],
    }, zoom=15, color=match_row["location_colour"], size = 25)