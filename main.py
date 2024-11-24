import streamlit as st

report_page = st.Page("reports.py", title="Match Reports", icon=":material/info:")
team_page = st.Page("team.py", title="Team Stats", icon=":material/info:")

pg = st.navigation([report_page, team_page])
pg.run()