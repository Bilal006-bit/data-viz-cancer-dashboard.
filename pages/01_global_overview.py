import streamlit as st
import plotly.express as px
from utils import load_data, apply_swd_layout

st.title("Global Cancer Mortality Overview")
st.markdown("Explore the macro trends of cancer mortality across the globe from 1990 to 2019.")

df = load_data()
df_world = df[df['Entity'] == 'World']

# Extract top cancers globally for the selected year
selected_year = st.slider("Select Year", 1990, 2019, 2019)
top5 = df_world[df_world['Year'] == selected_year].groupby('Cancer_Type')['Deaths'].sum().nlargest(5).index

# Build trend visualization
df_q1 = df_world[df_world['Cancer_Type'].isin(top5)]
fig = px.line(df_q1, x='Year', y='Deaths', color='Cancer_Type',
              title='Tracheal, bronchus, and lung cancers drive the highest mortality globally')

# Highlight top cancer type, grey out others
color_map = {c: ('#D55E00' if 'bronchus' in c.lower() else '#CCCCCC') for c in top5}
fig.update_traces(line=dict(width=3))
for trace in fig.data:
    trace.line.color = color_map.get(trace.name, '#CCCCCC')

fig = apply_swd_layout(fig)
fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

st.plotly_chart(fig, use_container_width=True)
