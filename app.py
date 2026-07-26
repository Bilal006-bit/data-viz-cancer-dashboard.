import streamlit as st

st.set_page_config(page_title="Global Cancer Trends", layout="wide", page_icon="🌍")

pg = st.navigation([
    st.Page("pages/01_interactive_map.py", title="Global Spread (Map)", icon="🗺️"),
    st.Page("pages/02_demographic_trends.py", title="Long-term Trends", icon="📈"),
    st.Page("pages/03_regional_shifts.py", title="Regional Shifts", icon="📊"),
    st.Page("pages/04_cancer_correlations.py", title="Cancer Correlations", icon="🔗"),
    st.Page("pages/05_top_burdens.py", title="Top Mortality Burdens", icon="⚠️"),
])

pg.run()
