import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from display import build_map, scorecard
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
    st.dataframe(match_df)
    match_row = match_df.iloc[0]

    if match_row["mv_home_display"]:
        scorecard(match_row=match_row, mv=True)
        scorecard(match_row=match_row, mv=False)
    else:
        scorecard(match_row=match_row, mv=False)
        scorecard(match_row=match_row, mv=True)
    # todo mv vs mv
        
    st.markdown(f"<br>", unsafe_allow_html=True)
    
    col_text, col_map = st.columns([32,30])
    with col_text:
        st.markdown(f"""
                    <b>Date:</b> {match_row['Date_Full']}
                    <br><b>KO:</b> {match_row['Time_Display']}
                    <br><b>Age Group:</b> {match_row['age_group']}
                    <br><b>Competition:</b> {match_row['competition_main_name']}{' - ' + match_row['competition_sub_name'] if match_row['competition_sub_name'] != '' else ''}
                    <br><b>Venue:</b> {match_row['location_name']}
            """, unsafe_allow_html=True)
 
        col_weather_img, col_weather_desc = st.columns([10,42])
        with col_weather_img:
            st.image(match_row['weather_image'], width=50)
        with col_weather_desc:
             st.markdown(f"""
                    <p>
                    <b>Weather:</b> {match_row['weather_type']}
                    <br><b>Temperature:</b> {match_row['temperature']}°C
                """, unsafe_allow_html=True)
        
        if match_row['potm'] and match_row['potm'] != "":
            st.markdown(f"""<br><b>Player of the Match:</b> {match_row['potm']}
            """, unsafe_allow_html=True)
 
    with col_map:
        build_map(match_row)
            
    match_report_col, _, lineup_col = st.columns([30,3,7])

    with match_report_col:
        if match_row['match_report'] != "":
            st.markdown(f"<p><b>Match Report:</b><br>", unsafe_allow_html=True)
            st.markdown(f"{match_row['match_report']}".replace("\n", "<br>"), unsafe_allow_html=True)
    # todo mv vs mv
    with lineup_col:
        st.markdown("<b>Squad:</b>", unsafe_allow_html=True)
        st.markdown(match_row['players'].replace("\n", "<br>"), unsafe_allow_html=True)
        # todo mv vs mv
    
    # Milestones
    if match_row['team_milestones'] and match_row['team_milestones'] != "":
        st.markdown("<b>Team Milestones:</b>", unsafe_allow_html=True)
        st.markdown(match_row['team_milestones'].replace("* ", "").replace("\n", "<br>"), unsafe_allow_html=True)
    if match_row['player_milestones'] and match_row['player_milestones'] != "":
        st.markdown("<b>Player Milestones:</b>", unsafe_allow_html=True)
        st.markdown(match_row['player_milestones'].replace("* ", "").replace("\n", "<br>"), unsafe_allow_html=True)
    if match_row['squad_milestones'] and match_row['squad_milestones'] != "":
        st.markdown("<b>Squad Milestones:</b>", unsafe_allow_html=True)
        st.markdown(match_row['squad_milestones'].replace("* ", "").replace("\n", "<br>"), unsafe_allow_html=True)

    # todo mv vs mv
    # todo mv vs mv