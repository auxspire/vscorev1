
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="VScor", page_icon="⚽")

if "user" not in st.session_state:
    switch_page("1_Login")
else:
    role = st.session_state.get("role", "")
    if role == "admin":
        switch_page("2_Admin_Dashboard")
    else:
        st.write("Welcome to VScor!")
        st.write("Role-based dashboards coming soon.")
