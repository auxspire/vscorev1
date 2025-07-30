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

st.set_page_config(page_title="Login - VScor", page_icon="⚽")

st.title("⚽ VScor Login / Signup")

auth_mode = st.radio("Choose action", ["Login", "Signup"], horizontal=True)

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if auth_mode == "Signup":
    role = st.selectbox("Select Role", ["admin", "match_scorer", "viewer", "player"])

if st.button(auth_mode):
    try:
        if auth_mode == "Signup":
            user = supabase.auth.sign_up({"email": email, "password": password})
            st.success("Signup successful.")
            uid = user.user.id
            # Insert into users table
            supabase.table("users").insert({"id": uid, "email": email, "role": role}).execute()
            st.success("User profile created. Please log in.")

        else:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state["user"] = user.user
            uid = user.user.id
            profile = supabase.table("users").select("*").eq("id", uid).single().execute()
            if profile.data:
                st.session_state["role"] = profile.data["role"]
                st.rerun()
            else:
                st.error("User profile not found.")
    except Exception as e:
        st.error(f"Auth failed: {e}")

if "user" in st.session_state:
    st.info(f"Logged in as {st.session_state['user'].email} ({st.session_state.get('role', 'Unknown')})")
    st.write("Use the sidebar to navigate.")