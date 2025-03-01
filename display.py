import base64
import folium
import pandas as pd
from pathlib import Path
import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.stylable_container import stylable_container
from streamlit_folium import st_folium, folium_static

from style import match_report_mobile_style, pitch_style, scorecard_style, scorecard_mobile_style


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
        goals = match_row['goals_for_display']
    else: 
        badge_image = match_row['badge_image']
        team_name = match_row['Opposition']
        goals = match_row['goals_against_display']
        
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


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = f'<img src="data:image/png;base64,{img_to_bytes(img_path)}" style="width: 60px; height: auto;">'
    return img_html


def scorecard_mobile(match_row: pd.Series, home: bool=True) -> None:
    """ 
    Display scorecard
    """
    print(match_row)
    ### Scorecard ###
    if home:
        badge_image = "images/clubs/merseyvalley.png"
        team_name = f"Mersey Valley {match_row['Team']}"
        goals = match_row['goals_for_display']
        scorers_formatted = match_row['scorers_formatted'].replace('\n', '<br>')
        scorers = f"<p class='scorers-text-mob'>{scorers_formatted}</p>"
        
    else: 
        badge_image = match_row['badge_image']
        team_name = match_row['Opposition']
        goals = match_row['goals_against_display']
        scorers = ""
        
    # Use markdown for layout instead of st.columns
    st.markdown(scorecard_mobile_style, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="container-mob">
        <div style="display: flex; align-items: center;">
            {img_to_html(badge_image)}
            <p class="team-text-mob" style="margin-left: 10px;">{team_name}</p>
        </div>
        <p class="goals-text-mob">{goals}</p>
    </div>
    {scorers}
    """, unsafe_allow_html=True)
 
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


def match_report(match_row: pd.Series, away=None) -> None:
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
                    <br><b>KO:</b> {match_row['Time']}
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
        if match_row['match_report'] != "":
            st.markdown(f"<br><b>Match Details:</b><br>{match_row['match_report']}".replace("\n", "<br>"), unsafe_allow_html=True)
        if away is not None:
            st.markdown(f"{away}".replace("\n", "<br>"), unsafe_allow_html=True)
        
    with col_map:
        build_map(match_row)
    
    return


def match_report_mobile(match_row: pd.Series, away=None) -> None:
    """
    Build & display the Match Report for Mobile
    """
    st.markdown(f"<br><br>", unsafe_allow_html=True)
    st.markdown("## Match Report:")
    st.markdown(f"""
                    <p>
                    <b>Date:</b> {match_row['formatted_date']}
                    <br><b>Age Group:</b> {match_row['AgeGroup']}
                    <br><b>Competition:</b> {match_row['Competition']}
                    <br><b>KO:</b> {match_row['Time']}
                    <br><b>Venue:</b> {match_row['Location']}
                """, unsafe_allow_html=True)
    build_map(match_row)
    
    # Weather
    st.markdown(match_report_mobile_style, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="container-mr-mob">
        <div style="display: flex; align-items: center;">
            {img_to_html(match_row['weather_image'])}
            <p class="weather-text-mob" style="margin-left: 40px;"><b>Weather:</b> {match_row['weather_description']}
                <br><b>Temperature:</b> {match_row['temperature']}°C</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Match Report
    if match_row['match_report'] != "":
        st.markdown(f"<br><b>Match Details:</b><br>{match_row['match_report']}".replace("\n", "<br>"), unsafe_allow_html=True)
    if away is not None:
        st.markdown(f"{away}".replace("\n", "<br>"), unsafe_allow_html=True)
        
    
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


def lineups(match_row: pd.Series, mobile_site: bool) -> None:
    """
    Build Lineup and team sheet output
    """
    col_text, col_graphic = st.columns([1,3])
    with col_text:
        if match_row['lineup'] != "":
            st.markdown(f"**{match_row['Team']} Lineup:**<br>{match_row['lineup']}".replace("\n", "<br>"), unsafe_allow_html=True)
            if match_row['subs_list'] != "":
                st.markdown(f"**Subs:**<br>{match_row['subs_list']}".replace("\n", "<br>"), unsafe_allow_html=True)   
        else:
            st.markdown(f"**{match_row['Team']} Squad:**<br>{match_row['squad_list']}".replace("\n", "<br>"), unsafe_allow_html=True)   
    
    with col_graphic:
        if mobile_site is False and match_row['lineup'] != "":  
            teamsheet_graphic(match_row)
