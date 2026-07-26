import streamlit as st
import plotly.express as px
from utils import load_data, apply_swd_layout

st.title("Regional Shifts Comparison")
st.markdown("Compare the burden of a specific cancer type across multiple countries simultaneously.")

df = load_data()
df_countries = df[df['Entity'] != 'World']

col1, col2, col3 = st.columns(3)
with col1:
    selected_cancer = st.selectbox("Select Cancer Type", df_countries['Cancer_Type'].unique(), index=4)
with col2:
    selected_year = st.slider("Select Year", 1990, 2019, 2019)
with col3:
    default_countries = ['United States', 'China', 'India', 'Brazil', 'Germany']
    selected_countries = st.multiselect("Select Countries", df_countries['Entity'].unique(), default=default_countries)

if selected_countries:
    df_filtered = df_countries[(df_countries['Year'] == selected_year) & 
                               (df_countries['Cancer_Type'] == selected_cancer) & 
                               (df_countries['Entity'].isin(selected_countries))]
    
    # Sort for visual hierarchy
    df_filtered = df_filtered.sort_values('Deaths', ascending=False)
    
    fig = px.bar(df_filtered, x='Entity', y='Deaths', 
                 title=f'{selected_cancer} cancer deaths across selected regions in {selected_year}',
                 color_discrete_sequence=['#CC79A7'])
    
    fig = apply_swd_layout(fig)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please select at least one country.")
