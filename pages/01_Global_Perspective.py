import streamlit as st
import plotly.express as px
from utils import load_data, apply_swd_layout

st.title("Global Perspective: Spread & Shifts")
st.markdown("Explore the macro-level impact of various cancer types across the world. Use the filters below to isolate specific years and diseases.")

df = load_data()
df_countries = df[df['Entity'] != 'World']

st.markdown("### 1. Geographic Spread")
col1, col2 = st.columns(2)
with col1:
    selected_year = st.slider("Select Year for Map", 1990, 2019, 2019)
with col2:
    selected_cancer = st.selectbox("Select Cancer Type", df_countries['Cancer_Type'].unique(), index=10)

df_map = df_countries[(df_countries['Year'] == selected_year) & (df_countries['Cancer_Type'] == selected_cancer)]

# Analytical Metrics
if not df_map.empty:
    total_deaths = df_map['Deaths'].sum()
    worst_hit = df_map.loc[df_map['Deaths'].idxmax()]
    st.markdown(f"**Insight:** In {selected_year}, {selected_cancer} caused **{total_deaths:,.0f}** recorded deaths globally. The hardest hit nation in absolute terms was **{worst_hit['Entity']}** with {worst_hit['Deaths']:,.0f} deaths.")

    fig_map = px.choropleth(df_map, locations="Entity", locationmode='country names', color="Deaths",
                            hover_name="Entity", color_continuous_scale="Reds",
                            title=f"Global distribution of {selected_cancer} cancer deaths in {selected_year}")
    fig_map.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
                          margin=dict(l=0, r=0, t=50, b=0), plot_bgcolor='white')
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning(f"No data available for {selected_cancer} in {selected_year}.")

st.divider()

st.markdown("### 2. Regional Shifts Comparison")
st.markdown("Compare the absolute burden of a specific cancer type across selected nations.")
col3, col4, col5 = st.columns(3)
with col3:
    shift_cancer = st.selectbox("Compare Cancer Type", df_countries['Cancer_Type'].unique(), index=4, key="shift_cancer")
with col4:
    shift_year = st.slider("Select Year", 1990, 2019, 2019, key="shift_year")
with col5:
    default_countries = ['United States', 'China', 'India', 'Brazil', 'Germany']
    shift_countries = st.multiselect("Select Countries", df_countries['Entity'].unique(), default=default_countries)

if shift_countries:
    df_shift = df_countries[(df_countries['Year'] == shift_year) & 
                            (df_countries['Cancer_Type'] == shift_cancer) & 
                            (df_countries['Entity'].isin(shift_countries))]
    df_shift = df_shift.sort_values('Deaths', ascending=False)
    
    fig_bar = px.bar(df_shift, x='Entity', y='Deaths', 
                     title=f'{shift_cancer} cancer deaths across selected regions in {shift_year}',
                     color_discrete_sequence=['#CC79A7'])
    fig_bar = apply_swd_layout(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("Select at least one country to view the comparison.")
