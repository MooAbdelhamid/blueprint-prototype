import streamlit as st

st.title("Import Data")

st.write(
    """
    Upload a CSV or Excel file to import your
    business data into Blueprint.
    """
)

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    st.write("File size:", uploaded_file.size, "bytes")
