
import streamlit as st
from utils.supabase_client import get_supabase_client

supabase = get_supabase_client()

st.title("⚽ VScor - Login / Signup")

auth_mode = st.radio("Choose action", ["Login", "Signup"], horizontal=True)

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button(auth_mode):
    try:
        if auth_mode == "Signup":
            user = supabase.auth.sign_up({"email": email, "password": password})
            st.success("Signup successful. Please log in.")
        else:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state["user"] = user.user
            st.success("Login successful!")

            # Fetch role from users table
            uid = user.user.id
            profile = supabase.table("users").select("*").eq("id", uid).single().execute()
            if profile.data:
                st.session_state["role"] = profile.data["role"]
                st.switch_page("pages/2_Admin_Dashboard.py")
            else:
                st.error("User role not found.")
    except Exception as e:
        st.error(f"Auth failed: {e}")
