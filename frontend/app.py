import streamlit as st

st.set_page_config(page_title="Blueprint", page_icon="📊", layout="wide")


st.title("Blueprint")

st.subheader("Your business data. One place.")

st.write(
    """
    Connect your business data, import your files,
    and transform your raw information into structured data.
    """
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("Import your data")
    st.write(
        """
        Upload CSV or Excel files and bring your
        business data into Blueprint.
        """
    )

    if st.button("Import Data", type="primary"):
        st.switch_page("pages/import_data.py")


with col2:
    st.header("Understand your business")
    st.write(
        """
        Once your data is imported, Blueprint can
        organize and analyze it.
        """
    )
