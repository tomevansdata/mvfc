import streamlit as st

result_page = st.Page("results.py", title="Results", icon=":material/info:")
report_page = st.Page("reports.py", title="Match Reports", icon=":material/info:")
team_page = st.Page("team.py", title="Team Stats", icon=":material/info:")

pg = st.navigation([result_page, report_page, team_page], position="top")
pg.run()