import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from streamlit_folium import st_folium

from display import chart_results_by_team, chart_goals_by_location, chart_league_table
from functions import get_match_list_detailed, apply_filters
from style import match_report_mobile_style, pitch_style, scorecard_style, scorecard_mobile_style


st.set_page_config(layout="wide", page_title='MVFC: Team Stats', page_icon = 'images/clubs/merseyvalley.png')

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

### Get Data
df = get_match_list_detailed()

### Apply reusable filters
filtered_df, filters = apply_filters(df)

#### CHART: Results by Team
with st.expander("Team Results", expanded=False):
    chart_results_by_team(filtered_df)

#### LEAGUE TABLE
with st.expander("League Table", expanded=True):
    chart_league_table(filtered_df)

#### CHART: Goals by Location
with st.expander("Goals by Location", expanded=True):
    m = chart_goals_by_location(filtered_df)
    if m is not None:
        # explicit pixel height prevents the expander from growing indefinitely
        st_folium(m, use_container_width=False, width=550, height=420, key="goals_map")


#### GOALS Scored Home and Away

#### GOALS Scored and Conceded

#### OPPONENTS Record

