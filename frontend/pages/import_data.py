import streamlit as st

from database.tenant_manager import TenantDatabaseManager
from etl.csv.pipeline import CSVPipeline

# SETUP
database = "blueprint-main"
manager = TenantDatabaseManager()
pipeline = CSVPipeline(manager)

# ------------------------------------
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
    pipeline.run(database, uploaded_file)
    st.success("File uploaded to database")
