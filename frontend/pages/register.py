"""
Register page demo
"""

import streamlit as st

st.title("Register")

username = st.text_input("Username")
email = st.text_input("Email")
passowrd = st.text_input("Password", type="password")

if st.button("Register"):
    st.write("Registered")
    st.switch_page("login.py")
