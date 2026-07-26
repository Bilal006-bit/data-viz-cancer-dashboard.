import streamlit as st
import plotly.express as px
from utils import load_data, apply_swd_layout

st.title("Interactive Global Spread")
st.markdown("Visualize the global footprint of different cancer types over the last 30 years.")

df = load_data()
df_countries = df[df['Entity'] != 'World']

col1, col2 = st.columns(2)
with col1:
    selected_year = st.slider("Select Year", 1990, 2019, 2019)
with col2:
    selected_cancer = st.selectbox("Select Cancer Type", df_countries['Cancer_Type'].unique(), index=10)

df_filtered = df_countries[(df_countries['Year'] == selected_year) & (df_countries['Cancer_Type'] == selected_cancer)]

fig = px.choropleth(df_filtered, locations="Entity", locationmode='country names', color="Deaths",
                    hover_name="Entity", color_continuous_scale="Reds",
                    title=f"Global distribution of {selected_cancer} cancer deaths in {selected_year}")

fig.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
                  margin=dict(l=0, r=0, t=50, b=0), plot_bgcolor='white')
st.plotly_chart(fig, use_container_width=True)
