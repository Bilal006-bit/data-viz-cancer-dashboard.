import streamlit as st

st.set_page_config(page_title="Global Cancer Trends", layout="wide", page_icon="🌍")

pg = st.navigation([
    st.Page("pages/01_Global_Perspective.py", title="Global Perspective", icon="🗺️"),
    st.Page("pages/02_Demographics_and_Correlations.py", title="Demographics & Insights", icon="🔬"),
])

pg.run()
