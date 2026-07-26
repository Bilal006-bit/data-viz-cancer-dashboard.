import streamlit as st
import plotly.express as px
from utils import load_data, apply_swd_layout

st.title("Cancer Burden Correlations")
st.markdown("Discover correlations between two different cancer types across the world.")

df = load_data()
df_countries = df[df['Entity'] != 'World']

col1, col2, col3 = st.columns(3)
with col1:
    cancer_x = st.selectbox("X-Axis Cancer Type", df_countries['Cancer_Type'].unique(), index=list(df_countries['Cancer_Type'].unique()).index('Breast'))
with col2:
    cancer_y = st.selectbox("Y-Axis Cancer Type", df_countries['Cancer_Type'].unique(), index=list(df_countries['Cancer_Type'].unique()).index('Colon and rectum'))
with col3:
    selected_year = st.slider("Select Year", 1990, 2019, 2019)

df_year = df_countries[df_countries['Year'] == selected_year]
df_x = df_year[df_year['Cancer_Type'] == cancer_x][['Entity', 'Deaths']].rename(columns={'Deaths': cancer_x})
df_y = df_year[df_year['Cancer_Type'] == cancer_y][['Entity', 'Deaths']].rename(columns={'Deaths': cancer_y})

df_merged = df_x.merge(df_y, on='Entity').dropna()

fig = px.scatter(df_merged, x=cancer_x, y=cancer_y, hover_name='Entity',
                 log_x=True, log_y=True,
                 title=f'Correlation between {cancer_x} and {cancer_y} ({selected_year})',
                 labels={cancer_x: f'{cancer_x} Deaths (Log)', cancer_y: f'{cancer_y} Deaths (Log)'},
                 color_discrete_sequence=['#009E73'])

fig = apply_swd_layout(fig)
st.plotly_chart(fig, use_container_width=True)
