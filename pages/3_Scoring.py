import streamlit as st
import sys, os
from datetime import datetime
from supabase_client import get_supabase_client

with st.sidebar:
    st.title("⚽ VScor")
    if "user" in st.session_state:
        st.write(f"Logged in as: {st.session_state['user'].email}")
        menu = st.radio("Navigation", ["Admin Dashboard", "Match Scoring", "Logout"])
        if menu == "Admin Dashboard":
            st.switch_page("pages/2_Admin_Dashboard.py")
        elif menu == "Match Scoring":
            st.switch_page("pages/3_Scoring.py")
        elif menu == "Logout":
            st.session_state.clear()
            st.rerun()
    else:
        st.info("Please log in first.")

with st.sidebar:
    st.title("⚽ VScor")
    if "user" in st.session_state:
        st.write(f"Logged in as: {st.session_state['user'].email}")
        menu = st.radio("Navigation", ["Admin Dashboard", "Match Scoring", "Logout"])
        if menu == "Admin Dashboard":
            st.switch_page("pages/2_Admin_Dashboard.py")
        elif menu == "Match Scoring":
            st.switch_page("pages/3_Scoring.py")
        elif menu == "Logout":
            st.session_state.clear()
            st.rerun()
    else:
        st.info("Please log in first.")


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

supabase = get_supabase_client()
st.set_page_config(page_title="Match Scoring - VScor", page_icon="⚽")
st.title("⚽ Match Scoring")

if "user" not in st.session_state or st.session_state.get("role") not in ["admin", "match_scorer"]:
    st.error("You must be an admin or scorer to access this page.")
    st.stop()

# Select Tournament and Teams
tournaments = supabase.table("tournaments").select("id, name").execute().data
tournament_map = {t["name"]: t["id"] for t in tournaments}
selected_tournament = st.selectbox("Tournament", list(tournament_map.keys()))

teams = supabase.table("teams").select("id, name").eq("tournament_id", tournament_map[selected_tournament]).execute().data
team_map = {t["name"]: t["id"] for t in teams}
selected_teams = st.multiselect("Select 2 Teams for Match", list(team_map.keys()), max_selections=2)

if len(selected_teams) == 2:
    match_name = st.text_input("Match Name", f"{selected_teams[0]} vs {selected_teams[1]}")
    if st.button("Start Match"):
        match_insert = supabase.table("matches").insert({
            "tournament_id": tournament_map[selected_tournament],
            "match_name": match_name,
            "match_type": "custom",
            "custom_team_size": len(team_map),
            "match_start": datetime.utcnow(),
            "status": "live"
        }).execute()
        match_id = match_insert.data[0]["id"]

        # Add teams to match
        for team in selected_teams:
            supabase.table("match_participants").insert({
                "match_id": match_id,
                "team_id": team_map[team]
            }).execute()

        st.success(f"Match '{match_name}' started!")

# Log Event (example UI)
st.subheader("Log Match Event")
event_types = ["goal", "freekick", "corner", "foul", "penalty", "save", "shot_on", "shot_off", "offside"]
match_id_input = st.text_input("Match ID")
team_id_input = st.text_input("Team ID")
player_id_input = st.text_input("Player ID")
event_type = st.selectbox("Event Type", event_types)
event_minute = st.number_input("Minute", min_value=0, max_value=120)
event_second = st.number_input("Second", min_value=0, max_value=59)

if st.button("Add Event"):
    total_seconds = event_minute * 60 + event_second
    supabase.table("events").insert({
        "match_id": match_id_input,
        "team_id": team_id_input,
        "player_id": player_id_input,
        "event_type": event_type,
        "event_time": f"00:{event_minute:02}:{event_second:02}"
    }).execute()
    st.success("Event logged!")