import altair as alt
import folium
import math
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from style import match_report_mobile_style, pitch_style, scorecard_style, scorecard_mobile_style, scorecard_mini_style


def scorecard(match_row: pd.Series, mv: bool = True) -> None:
    """
    Display a match scorecard with team badge, name, scorers, and goals.

    Parameters
    ----------
    match_row : pd.Series
        A pandas Series containing match data with columns:
        'mv_team', 'mv_goals', 'scorers', 'opp_badge_link', 'opp_team', 'opp_goals'.
    mv : bool, optional
        If True (default), display Mersey Valley team data. If False, display opponent data.

    Returns
    -------
    None
    """
    col_badge, col_team, col_score = st.columns([1, 4, 2])
    st.markdown(scorecard_style, unsafe_allow_html=True)

    if mv:
        badge_image = "images/clubs/merseyvalley.png"
        team_name = f"Mersey Valley {match_row['mv_team']}"
        goals = match_row['mv_goals']
    else:
        badge_image = match_row['opp_badge_link']
        team_name = match_row['opp_team']
        goals = match_row['opp_goals']

    with col_badge:
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.image(badge_image, width=80)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_team:
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.markdown(f"<p class='team-text'>{team_name}</p>", unsafe_allow_html=True)

        if mv:
            scorers_formatted = match_row['scorers'].replace("\n", "<br>")
            st.markdown(f"<div class='scorers-text'>{scorers_formatted}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_score:
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.markdown(f"<p class='goals-text'>{goals}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    return

def scorecard_mini(match_row: pd.Series) -> None:
    """
    Display a match scorecard with team badge, name, and goals.

    Parameters
    ----------
    match_row : pd.Series
        A pandas Series containing m atch data with columns:
        'mv_team', 'mv_goals', 'scorers', 'opp_badge_link', 'opp_team', 'opp_goals'.
    Returns
    -------
    None
    """
    col_badge, col_team, col_score, _ = st.columns([1, 5, 1, 1])
    st.markdown(scorecard_mini_style, unsafe_allow_html=True)

    if match_row["home_away"] in ["Home", "Neutral"]:
        home_badge_image = "images/clubs/merseyvalley.png"
        home_team_name = f"Mersey Valley {match_row['mv_team']}"
        home_goals = match_row['mv_goals_string']
        
        away_badge_image = match_row['opp_badge_link']
        away_team_name = match_row['opp_team']
        away_goals = match_row['opp_goals_string']
    else:
        home_badge_image = match_row['opp_badge_link']
        home_team_name = match_row['opp_team']
        home_goals = match_row['opp_goals_string']
        
        away_badge_image = "images/clubs/merseyvalley.png"
        away_team_name = f"Mersey Valley {match_row['mv_team']}"
        away_goals = match_row['mv_goals_string']

    with col_badge:
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.image(home_badge_image, width=25)
        st.image(away_badge_image, width=25)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_team:
        st.markdown("<div class='column-container'>", unsafe_allow_html=True)
        st.markdown(home_team_name, unsafe_allow_html=True)
        st.markdown(away_team_name, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_score:
        st.markdown("<div class='goals-text'>", unsafe_allow_html=True)
        st.markdown(home_goals, unsafe_allow_html=True)
        st.markdown(away_goals, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    return


def build_map(match_row: pd.Series) -> None:
    """
    Build and display a map showing the match location.

    Parameters
    ----------
    match_row : pd.Series
        A pandas Series containing match data with columns:
        'lat', 'lon', 'location_name', 'location_colour'.
    Returns
    -------
    None
    """
    latitude = match_row['lat'] 
    longitude = match_row['lon']
    colour = match_row['location_colour']
    
    mymap = folium.Map(
                location=[latitude, longitude],
                zoom_start=13, 
                tiles='OpenStreetMap',
            ) 

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=10, 
        color='black',
        fill=True,
        fill_color=colour, 
        fill_opacity=0.9
    ).add_to(mymap)

    st_folium(mymap, width=300, height=275)


def chart_league_table(df: pd.DataFrame) -> None:
    """
    Create and display a league table showing team standings.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing match results with columns 'team', 'mv_points', 'mv_goal_diff', 'mv_goals_for'.

    Returns
    -------
    None
        Displays a table dataframe via Streamlit.
    """
    league_table = (
        df.groupby("team").agg(
            P=("team", "count"),
            W=("mv_win_ind", "sum"),
            L=("opp_win_ind", "sum"),
            D=("draw_ind", "sum"),
            U=("unknown_ind", "sum"),
            GF=("mv_goals", "sum"),
            GA=("opp_goals", "sum"),
        )
        .reset_index()
    )
    
    # Calculate points: wins × 3 + draws × 1
    league_table["Pts"] = league_table["W"] * 3 + league_table["D"]
    
    # Calculate goal difference
    league_table["GD"] = league_table["GF"] - league_table["GA"]

    # Reorder columns for better display
    league_table = league_table[["team", "P", "W", "D", "L", "U", "GF", "GA", "GD", "Pts"]]
    
    # Sort by points descending
    league_table = league_table.sort_values("Pts", ascending=False).reset_index(drop=True)
    
    # Rename team column for display
    league_table = league_table.rename(columns={"team": "Team"})
    
    # Convert to integer for cleaner display
    numeric_cols = ["P", "W", "D", "L", "U", "GF", "GA", "GD", "Pts"]
    league_table[numeric_cols] = league_table[numeric_cols].astype(int)
    
    # Display with styling
    st.dataframe(
        league_table,
        width="stretch",
        hide_index=True,
        column_config={
            "Team": st.column_config.TextColumn(width=120),
            "P": st.column_config.NumberColumn(width=35),
            "W": st.column_config.NumberColumn(width=35),
            "D": st.column_config.NumberColumn(width=35),
            "L": st.column_config.NumberColumn(width=35),
            "U": st.column_config.NumberColumn(width=35),
            "GF": st.column_config.NumberColumn(width=35),
            "GA": st.column_config.NumberColumn(width=35),
            "GD": st.column_config.NumberColumn(width=35),
            "Pts": st.column_config.NumberColumn(width=40),
        }
    )



def chart_results_by_team(df: pd.DataFrame) -> None:
    """
    Create and display a stacked bar chart of team results (wins, losses, draws).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing match results with columns 'team', 'mv_win_ind', 'opp_win_ind', 'draw_ind'.

    Returns
    -------
    None
        Displays an Altair chart via Streamlit.
    """
    df_team = (
        df.groupby("team", as_index=False)
        .agg(
            win_count=("mv_win_ind", "sum"),
            loss_count=("opp_win_ind", "sum"),
            draw_count=("draw_ind", "sum")
        )
    )

    df_long = df_team.melt(
        id_vars="team",
        value_vars=["win_count", "loss_count", "draw_count"],
        var_name="result",
        value_name="games"
    )

    df_long["result"] = df_long["result"].map({
        "win_count": "Win",
        "loss_count": "Lose",
        "draw_count": "Draw",
    })

    res_order = {"Win": 0, "Lose": 1, "Draw": 2}
    df_long["order"] = df_long["result"].map(res_order)
    df_long = df_long[df_long["games"] > 0]

    df_totals = (
        df_long.groupby("team", as_index=False)["games"]
        .sum()
        .rename(columns={"games": "total"})
    )

    base = (
        alt.Chart(df_long)
        .transform_stack(
            as_=["stack_start", "stack_end"],
            stack="games",
            groupby=["team"],
            sort=[alt.SortField("order", order="ascending")],
        )
        .transform_calculate(middle=(alt.datum.stack_start + alt.datum.stack_end) / 2)
    )
    colour_scale = alt.Scale(
        domain=["Win", "Lose", "Draw"],
        range=["#E5AD32", "#000000", "#217F40"],
    )

    y_axis = alt.Y(
        "team:N",
        sort="descending",
        title=None,
        scale=alt.Scale(paddingInner=0.33),
    )
    bars = base.mark_bar().encode(
        y=y_axis,
        x=alt.X("stack_start:Q", title="Number of Games"),
        x2="stack_end:Q",
        color=alt.Color(
            "result:N",
            scale=colour_scale,
            legend=alt.Legend(
                title=None, orient="top", direction="horizontal", offset=20
            ),
        ),
        tooltip=[
            alt.Tooltip("team:N", title="Team"),
            alt.Tooltip("result:N", title="Result"),
            alt.Tooltip("games:Q", title="Games"),
        ],
    )
    segment_labels = base.mark_text(
        baseline="middle", align="center", fontWeight="bold", fontSize=12
    ).encode(
        y=y_axis,
        x=alt.X("middle:Q"),
        text=alt.Text("games:Q"),
        color=alt.condition(
            alt.datum.result == "Win",
            alt.value("black"),
            alt.value("white"),
        ),
    )
    total_labels = alt.Chart(df_totals).mark_text(
        align="left", dx=10, fontWeight="bold", fontSize=13
    ).encode(
        y=y_axis,
        x=alt.X("total:Q"),
        text=alt.Text("total:Q"),
    )
    chart = (
        (bars + segment_labels + total_labels)
        .properties(
            width=800,
            height=350,
        )
        .configure_axis(grid=False, domain=False, ticks=False)
        .configure_view(strokeWidth=0)
    )
    st.altair_chart(chart)


def chart_goals_by_location(df: pd.DataFrame) -> None:
    """
    Create and display a map of goals scored by location.

    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame containing match data with columns:
        'lat', 'lon', 'location_name', 'location_colour', 'mv_goals'.
    Returns
    ------- 
    None
    """
    df_grouped = (
        df
        .groupby(["lat", "lon", "location_name", "location_colour"], as_index=False)
        .agg(
            goals=("mv_goals", "sum")
        )
    )

    # Create base map (location/zoom will be overridden by fit_bounds)
    m = folium.Map(tiles="OpenStreetMap")

    # Keep track of bounds
    bounds = []

    for _, row in df_grouped.iterrows():
        #radius = row["goals"] * 3  # scale factor – tweak to taste
        
        radius = math.log(row["goals"] + 1) * 10

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radius,
            color=row["location_colour"],
            fill=True,
            fill_color=row["location_colour"],
            fill_opacity=0.6,
            popup=f"{row['location_name']}: {row['goals']} goals"
        ).add_to(m)

        bounds.append([row["lat"], row["lon"]])

    # Auto-zoom map to fit all points
    if bounds:
        m.fit_bounds(bounds)
    
    return m

