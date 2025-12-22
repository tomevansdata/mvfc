import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from functions import get_match_list, get_match_data, apply_filters
from style import match_report_mobile_style, pitch_style, scorecard_style, scorecard_mobile_style


st.set_page_config(layout="wide", page_title='MVFC: Results', page_icon = 'images/clubs/merseyvalley.png')

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

### Get Data ###
df = get_match_list()
# for m in matches:
#     if st.button(f"View report vs {m['opponent']}", key=m["match_id"]):
#         query_params = {"match_id" : str(m["match_id"])}
#         st.switch_page("reports.py", query_params=query_params)

### Apply reusable filters
filtered_df, filters = apply_filters(df)