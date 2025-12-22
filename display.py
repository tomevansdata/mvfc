import pandas as pd
import streamlit as st

from style import match_report_mobile_style, pitch_style, scorecard_style, scorecard_mobile_style


def scorecard(match_row: pd.Series, mv: bool=True) -> None:
    """ 
    Display scorecard
    """
    ### Scorecard ###
    col_badge, col_team, col_score, = st.columns([1, 4, 2])
    st.markdown(scorecard_style, unsafe_allow_html=True)

    if mv:   
        badge_image = "images/clubs/merseyvalley.png"
        team_name = f"Mersey Valley {match_row['mv_team']}"
        goals = match_row['mv_goals']
    else: 
        badge_image = match_row['opp_badge_link']
        team_name = match_row['opp_team']
        goals = match_row['opp_goals']
        
    # Column 1: Badge Image 
    with col_badge:
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.image(badge_image, width=80)
        st.markdown("</div>", unsafe_allow_html=True)

    # Column 2: Team Name/Scorers
    with col_team:  
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.markdown(f"<p class='team-text'>{team_name}</p>", unsafe_allow_html=True)
        
        if mv:
            scorers_formatted = match_row['scorers'].replace("\n", "<br>")
            st.markdown(f"<div class='scorers-text'>{scorers_formatted}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
    # Column 3: Goals Scored
    with col_score:
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.markdown(f"<p class='goals-text'>{goals}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    return
