"""
App front page demo
"""

import streamlit as st

st.set_page_config(page_title="BluePrint", layout="centered")

st.title("Welcome")

if st.button("Register"):
    st.switch_page("pages/register.py")

if st.button("Login"):
    st.switch_page("pages/login.py")
