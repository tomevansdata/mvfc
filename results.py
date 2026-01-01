import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from display import scorecard_mini
from functions import get_match_list_detailed, apply_filters
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
df = get_match_list_detailed()

### Apply reusable filters
filtered_df, filters = apply_filters(df)

filtered_df = filtered_df.sort_values(by="match_date", ascending=False).head(50)

for idx, (_, match_row) in enumerate(filtered_df.iterrows()):
    match_header = match_row["match_header"]
    match_id = match_row["match_id"]

    with st.expander(match_header):
        col1, col2 = st.columns([3, 1])

        with col1:
            html_content = f"""
            <div style="font-size: 14px; line-height: 1.4;">
                <div><strong>{match_row['competition_main_name']}{': ' +match_row['competition_sub_name'] if match_row['competition_main_name'] != 'Friendly' else ''}</strong></div>
                <div><strong>{match_row['Date_Full']}: {match_row['Time_Display']}</strong></div>
                <div><strong>Location: {match_row['location_name']}</strong></div>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
            
            scorecard_mini(match_row)
        
        with col2:
            if st.button("📋 View Report", key=f"report_{idx}_{match_id}"):
                query_params = {"match_id": str(match_id)}
                st.switch_page("reports.py", query_params=query_params)
            # Format scorers with line breaks
            scorers_html = match_row['scorers'].replace('\n', '<br>') if pd.notna(match_row['scorers']) else ''
            if scorers_html != '':
                html_content = f"""
                <div style="font-size: 14px; line-height: 1.4;">
                    <div style="margin-top: 8px;"><strong>Scorers:</strong></div>
                    <div>{scorers_html}</div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
