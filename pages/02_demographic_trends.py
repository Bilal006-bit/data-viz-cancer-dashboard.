import streamlit as st
import plotly.express as px
from utils import load_data, apply_swd_layout

st.title("Long-term Demographic Trends")
st.markdown("Track the trajectory of specific cancer types within any country.")

df = load_data()
df_countries = df[df['Entity'] != 'World']

col1, col2 = st.columns(2)
with col1:
    selected_country = st.selectbox("Select Country", df_countries['Entity'].unique(), index=list(df_countries['Entity'].unique()).index('United States'))
with col2:
    selected_cancers = st.multiselect("Select Cancer Types", df_countries['Cancer_Type'].unique(), default=['Stomach', 'Colon and rectum'])

if selected_cancers:
    df_filtered = df_countries[(df_countries['Entity'] == selected_country) & (df_countries['Cancer_Type'].isin(selected_cancers))]
    
    fig = px.line(df_filtered, x='Year', y='Deaths', color='Cancer_Type',
                  title=f'Cancer Mortality Trends in {selected_country} (1990 - 2019)',
                  color_discrete_sequence=['#0072B2', '#D55E00', '#009E73', '#CC79A7'])
    
    fig = apply_swd_layout(fig)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please select at least one cancer type to view trends.")
