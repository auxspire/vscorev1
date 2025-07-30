import streamlit as st
import sys, os
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

st.set_page_config(page_title="Admin Dashboard - VScor", page_icon="⚽")
st.title("⚽ Admin Dashboard")

if "user" not in st.session_state or st.session_state.get("role") != "admin":
    st.error("You must be logged in as an admin to access this page.")
    st.stop()

# SECTION: Add Tournament
st.subheader("➕ Add Tournament")
with st.form("add_tournament"):
    name = st.text_input("Tournament Name")
    location = st.text_input("Location")
    team_size = st.number_input("Team Size", min_value=5, max_value=11, value=11)
    duration = st.number_input("Match Duration (mins)", min_value=30, max_value=120, value=90)
    has_halves = st.checkbox("Include Halves", value=True)
    submitted = st.form_submit_button("Create Tournament")
    if submitted:
        supabase.table("tournaments").insert({
            "name": name,
            "location": location,
            "team_size": team_size,
            "match_duration": duration,
            "has_halves": has_halves,
            "created_by": st.session_state["user"].id
        }).execute()
        st.success("Tournament added!")

# SECTION: Add Team
st.subheader("🏟 Add Team to Tournament")
tournaments = supabase.table("tournaments").select("id, name").execute().data
tournament_options = {t['name']: t['id'] for t in tournaments}
selected_tournament = st.selectbox("Select Tournament", list(tournament_options.keys()))

with st.form("add_team"):
    team_name = st.text_input("Team Name")
    team_submit = st.form_submit_button("Add Team")
    if team_submit:
        supabase.table("teams").insert({
            "name": team_name,
            "tournament_id": tournament_options[selected_tournament]
        }).execute()
        st.success(f"Team '{team_name}' added to {selected_tournament}!")

# SECTION: Add Player to Team
st.subheader("👤 Add Player to Team")
teams = supabase.table("teams").select("id, name").eq("tournament_id", tournament_options[selected_tournament]).execute().data
team_map = {t["name"]: t["id"] for t in teams}
selected_team = st.selectbox("Select Team", list(team_map.keys()))

with st.form("add_player"):
    full_name = st.text_input("Player Full Name")
    email = st.text_input("Player Email")
    jersey_number = st.number_input("Jersey Number", min_value=1, max_value=99)
    position = st.selectbox("Position", ["GK", "DF", "MF", "FW"])
    submitted = st.form_submit_button("Add Player")
    if submitted:
        # Check if player exists by email
        player_query = supabase.table("players").select("*").eq("email", email).execute()
        if player_query.data:
            player_id = player_query.data[0]["id"]
        else:
            player_insert = supabase.table("players").insert({
                "full_name": full_name,
                "email": email
            }).execute()
            player_id = player_insert.data[0]["id"]

        # Assign to team
        supabase.table("team_players").insert({
            "player_id": player_id,
            "team_id": team_map[selected_team],
            "jersey_number": jersey_number,
            "position": position
        }).execute()
        st.success(f"{full_name} added to team {selected_team}.")