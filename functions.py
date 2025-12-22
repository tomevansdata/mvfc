import pandas as pd
import streamlit as st

from db import execute_query 


@st.cache_data(ttl="1h")
def get_match_list() -> pd.DataFrame:
    q = """
    SELECT 
        age_group, 
        CASE WHEN competition_main_name = 'Friendly' THEN 'Friendly' 
        ELSE concat(competition_main_name,': ', competition_sub_name) END AS competition,
        mv_team AS team,
        match_date, 
        match_header,
        match_id
    FROM workspace.mvfc.vw_match_facts;
    """
    return execute_query(q)


@st.cache_data(ttl="1h")
def get_match_data(match_id: int) -> pd.DataFrame:
    q = f"""
    SELECT 
        *
    FROM workspace.mvfc.vw_match_report
    wHERE match_id = {match_id};
    """
    return execute_query(q)


def apply_filters(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Reusable filter sidebar with persistent state across pages.
    Filters are stored in st.session_state and survive page navigation.
    Returns: (filtered_df, filter_dict)
    """
    # Initialize session state on first load
    if "age_group_filter" not in st.session_state:
        st.session_state.age_group_filter = "All"
    if "team_filter" not in st.session_state:
        st.session_state.team_filter = "All"
    if "competition_filter" not in st.session_state:
        st.session_state.competition_filter = "All"
    if "date_filter" not in st.session_state:
        st.session_state.date_filter = (df['match_date'].min(), df['match_date'].max())
    
    # Sidebar header with reset button
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        st.sidebar.markdown("### Filters")
    with col2:
        if st.sidebar.button("🔄 Reset", key="reset_filters"):
            st.session_state.age_group_filter = "All"
            st.session_state.team_filter = "All"
            st.session_state.competition_filter = "All"
            st.session_state.date_filter = (df['match_date'].min(), df['match_date'].max())
            st.rerun()
    
    # Filter controls (read from and update session state)
    st.session_state.age_group_filter = st.sidebar.selectbox(
        "Select Age Group:", 
        options=["All"] + sorted(df["age_group"].unique()),
        index=["All"] + sorted(df["age_group"].unique()).tolist().index(st.session_state.age_group_filter) 
              if st.session_state.age_group_filter in ["All"] + sorted(df["age_group"].unique()).tolist() else 0,
        key="age_group_filter"
    )
    
    st.session_state.team_filter = st.sidebar.selectbox(
        "Select Team:", 
        options=["All"] + sorted(df["team"].unique()),
        index=["All"] + sorted(df["team"].unique()).tolist().index(st.session_state.team_filter) 
              if st.session_state.team_filter in ["All"] + sorted(df["team"].unique()).tolist() else 0,
        key="team_filter"
    )
    
    st.session_state.competition_filter = st.sidebar.selectbox(
        "Select Competition:", 
        options=["All"] + sorted(df["competition"].unique()),
        index=["All"] + sorted(df["competition"].unique()).tolist().index(st.session_state.competition_filter) 
              if st.session_state.competition_filter in ["All"] + sorted(df["competition"].unique()).tolist() else 0,
        key="competition_filter"
    )
    
    st.session_state.date_filter = st.sidebar.slider(
        "Select Date:", 
        min_value=df['match_date'].min(), 
        max_value=df['match_date'].max(), 
        value=st.session_state.date_filter,
        format="DD/MM/YYYY",
        key="date_filter"
    )
    
    # Apply filters to dataframe
    filtered_df = df.copy()
    
    if st.session_state.age_group_filter != "All":
        filtered_df = filtered_df[filtered_df["age_group"] == st.session_state.age_group_filter]
    if st.session_state.team_filter != "All":
        filtered_df = filtered_df[filtered_df["team"] == st.session_state.team_filter]
    if st.session_state.competition_filter != "All":
        filtered_df = filtered_df[filtered_df["competition"] == st.session_state.competition_filter]
    
    try:
        start_date, end_date = st.session_state.date_filter
        filtered_df = filtered_df[(filtered_df['match_date'] >= start_date) & (filtered_df['match_date'] <= end_date)]
    except Exception:
        pass
    
    filter_dict = {
        "age_group": st.session_state.age_group_filter,
        "team_name": st.session_state.team_filter,
        "competition": st.session_state.competition_filter,
        "selected_date": st.session_state.date_filter
    }
    
    return filtered_df, filter_dict