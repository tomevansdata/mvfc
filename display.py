import folium
import pandas as pd
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_folium import st_folium, folium_static

from style import pitch_style, scorecard_style


def scorecard(match_row: pd.Series, home: bool=True) -> None:
    """ 
    Display scorecard
    """
    ### Scorecard ###
    col_badge, col_team, col_score, = st.columns([1, 4, 2])
    st.markdown(scorecard_style, unsafe_allow_html=True)

    if home:
        badge_image = "images/clubs/merseyvalley.png"
        team_name = f"Mersey Valley {match_row['Team']}"
        goals = match_row['goals_for']
    else: 
        badge_image = match_row['badge_image']
        team_name = match_row['Opposition']
        goals = match_row['goals_against']
        
    # Column 1: Badge Image 
    with col_badge:
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.image(badge_image, width=80)
        st.markdown("</div>", unsafe_allow_html=True)

    # Column 2: Team Name/Scorers
    with col_team:  
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.markdown(f"<p class='team-text'>{team_name}</p>", unsafe_allow_html=True)
        
        if home:
            scorers_formatted = match_row['scorers_formatted'].replace("\n", "<br>")
            st.markdown(f"<div class='scorers-text'>{scorers_formatted}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
    # Column 3: Goals Scored
    with col_score:
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.markdown(f"<p class='goals-text'>{goals}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    return

def build_map(match_row: pd.Series) -> None:    
    """
    Build map and circle marker for match location
    """
    latitude = match_row['lat'] 
    longitude = match_row['lon']
    colour = match_row['location_colour']
    
    mymap = folium.Map(
                location=[latitude, longitude], 
                zoom_start=13, 
                zoom_control=False,
                scrollWheelZoom=False,
                dragging=False
            ) 

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=10, 
        color='black', 
        fill=True,
        fill_color=colour, 
        fill_opacity=0.9
    ).add_to(mymap)

    folium_static(mymap, width=300, height=275)

    return


def match_report(match_row: pd.Series) -> None:
    """
    Build & display the Match Report
    """
    st.markdown("### Match Report:")
    
    col_text, col_map = st.columns([32,30])
    with col_text:
        st.markdown(f"""
                    <p>
                    <b>Date:</b> {match_row['formatted_date']}
                    <br><b>Age Group:</b> {match_row['AgeGroup']}
                    <br><b>Competition:</b> {match_row['Competition']}
                    <br><b>Venue:</b> {match_row['Location']}
            """, unsafe_allow_html=True)
 
        col_weather_img, col_weather_desc = st.columns([10,42])
        with col_weather_img:
            st.image(match_row['weather_image'], width=50)
        with col_weather_desc:
             st.markdown(f"""
                    <p>
                    <b>Weather:</b> {match_row['weather_description']}
                    <br><b>Temperature:</b> {match_row['temperature']}°C
                """, unsafe_allow_html=True)
        
        # Match Report
        st.markdown(f"<br><b>Match Details:</b><br>{match_row['match_report']}".replace("\n", "<br>"), unsafe_allow_html=True)
        
    with col_map:
        build_map(match_row)
    
    return


def teamsheet_graphic(match_row: pd.Series) -> None:
    """
    Build the teamsheet graphic
    """
    gk_image = "images/misc/gk.png"
    shirt_image = "images/misc/shirt.png"
        
    # Create the pitch container using stylable_container
    with stylable_container(key="pitch", css_styles=pitch_style):

        # Goalkeeper row
        _,_,_,_,gk,_,_,_,_ = st.columns(9)
        with gk:
            if match_row["GK"]:
                st.image(gk_image, width=60, caption=match_row['GK'])
        # Defenders row
        _,rdf,_,_,cdf,_,_,ldf,_ = st.columns(9)
        with rdf:
            if match_row["RDF"]:
                st.image(shirt_image, width=60, caption=match_row['RDF'])
        with cdf:
            if match_row["CDF"]:
                st.image(shirt_image, width=60, caption=match_row['CDF'])
        with ldf:
            if match_row["LDF"]:
                st.image(shirt_image, width=60, caption=match_row['LDF'])

        # Midfielders row
        _,rm,_,_,cm,_,_,lm,_ = st.columns(9)
        with rm:
            if match_row["RM"]:
                st.image(shirt_image, width=60, caption=match_row['RM'])
        with cm:
            if match_row["CM"]:
                st.image(shirt_image, width=60, caption=match_row['CM'])
        with lm:
            if match_row["LM"]:
                st.image(shirt_image, width=60, caption=match_row['LM'])

        # Attackers row
        _,ra,_,_,ca,_,_,la,_ = st.columns(9)
        with ra:
            if match_row["RA"]:
                st.image(shirt_image, width=60, caption=match_row['RA'])
        with ca:
            if match_row["CA"]:
                st.image(shirt_image, width=60, caption=match_row['CA'])
        with la:
            if match_row["LA"]:
                st.image(shirt_image, width=60, caption=match_row['LA'])


def lineups(match_row: pd.Series) -> None:
    """
    Build Lineup and team sheet output
    """
    col_text, col_graphic = st.columns([1,3])
    with col_text:
        st.markdown(f"**Lineup:**<br>{match_row['lineup']}".replace("\n", "<br>"), unsafe_allow_html=True)   
        if match_row['subs_list'] != "":
            st.markdown(f"**Subs:**<br>{match_row['subs_list']}".replace("\n", "<br>"), unsafe_allow_html=True)   
    
    with col_graphic:  
        teamsheet_graphic(match_row)
