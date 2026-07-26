import streamlit as st
import plotly.express as px
from utils import load_data, apply_swd_layout

st.title("Top Mortality Burdens")
st.markdown("Identify the deadliest cancer types for a specific region.")

df = load_data()
df_countries = df[df['Entity'] != 'World']

col1, col2 = st.columns(2)
with col1:
    selected_country = st.selectbox("Select Country/Region", ['World'] + list(df_countries['Entity'].unique()))
with col2:
    selected_year = st.slider("Select Year", 1990, 2019, 2019)

df_filtered = df[(df['Entity'] == selected_country) & (df['Year'] == selected_year)]
df_top10 = df_filtered.sort_values('Deaths', ascending=False).head(10)

# Highlight top cancer type, grey out others for SWD compliance
color_map = {c: ('#D55E00' if i == 0 else '#AAAAAA') for i, c in enumerate(df_top10['Cancer_Type'])}

fig = px.bar(df_top10, x='Deaths', y='Cancer_Type', orientation='h',
             title=f'Top 10 Deadliest Cancers in {selected_country} ({selected_year})',
             color='Cancer_Type', color_discrete_map=color_map)

fig = apply_swd_layout(fig)
fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig, use_container_width=True)
