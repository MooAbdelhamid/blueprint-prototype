"""
Register page demo
"""

import streamlit as st
from services.api_client import register_user

st.title("Register")

username = st.text_input("Username")
email = st.text_input("Email")
passowrd = st.text_input("Password", type="password")

if st.button("Register"):
    register_user(username, email, passowrd)
    st.write("Registered")
    st.switch_page("pages/login.py")
