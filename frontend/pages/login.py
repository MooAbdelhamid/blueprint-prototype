"""
Login page demo
"""

import streamlit as st

st.title("Login")

user = st.text_input("Username or Email")
passowrd = st.text_input("Password", type="password")

if st.button("Login"):
    st.write("Registered")
