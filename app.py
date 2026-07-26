import streamlit as st

# Configure global page settings
st.set_page_config(page_title="Global Cancer Trends", layout="wide", page_icon="🌍")

# Define multi-page navigation
pg = st.navigation([
    st.Page("pages/01_global_overview.py", title="Global Overview", icon="🗺️"),
    st.Page("pages/02_country_deepdive.py", title="Country Deep Dive", icon="📍"),
    st.Page("pages/03_demographics.py", title="Demographic Shifts", icon="👥"),
])

pg.run()
