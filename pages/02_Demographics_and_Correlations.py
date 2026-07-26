import streamlit as st
import plotly.express as px
from utils import load_data, apply_swd_layout

st.title("Demographics & Insights")
st.markdown("Dive deeper into specific country trends, deadliest burdens, and correlations between cancer types.")

df = load_data()
df_countries = df[df['Entity'] != 'World']

st.markdown("### 1. The Deadliest Burdens by Region")
col1, col2 = st.columns(2)
with col1:
    burden_country = st.selectbox("Select Country/Region", ['World'] + list(df_countries['Entity'].unique()), index=0)
with col2:
    burden_year = st.slider("Select Year", 1990, 2019, 2019, key="burden_year")

df_burden = df[(df['Entity'] == burden_country) & (df['Year'] == burden_year)]

if not df_burden.empty:
    df_top10 = df_burden.sort_values('Deaths', ascending=False).head(10)

    top_killer = df_top10.iloc[0]
    st.markdown(f"**Insight:** In {burden_year}, the leading cause of cancer mortality in **{burden_country}** was **{top_killer['Cancer_Type']}**, accounting for {top_killer['Deaths']:,.0f} deaths.")

    color_map = {c: ('#D55E00' if i == 0 else '#AAAAAA') for i, c in enumerate(df_top10['Cancer_Type'])}
    fig_burden = px.bar(df_top10, x='Deaths', y='Cancer_Type', orientation='h',
                        title=f'Top 10 Deadliest Cancers in {burden_country} ({burden_year})',
                        color='Cancer_Type', color_discrete_map=color_map)
    fig_burden = apply_swd_layout(fig_burden)
    fig_burden.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_burden, use_container_width=True)
else:
    st.warning(f"No data available for {burden_country} in {burden_year}.")

st.divider()

st.markdown("### 2. Long-term Demographic Trajectories")
col3, col4 = st.columns(2)
with col3:
    trend_country = st.selectbox("Select Country for Trends", df_countries['Entity'].unique(), index=list(df_countries['Entity'].unique()).index('United States'))
with col4:
    trend_cancers = st.multiselect("Select Cancer Types to Track", df_countries['Cancer_Type'].unique(), default=['Stomach', 'Colon and rectum', 'Breast', 'Prostate'])

if trend_cancers:
    df_trend = df_countries[(df_countries['Entity'] == trend_country) & (df_countries['Cancer_Type'].isin(trend_cancers))]
    fig_trend = px.line(df_trend, x='Year', y='Deaths', color='Cancer_Type',
                        title=f'Cancer Mortality Trajectories in {trend_country} (1990 - 2019)',
                        color_discrete_sequence=['#0072B2', '#D55E00', '#009E73', '#CC79A7'])
    fig_trend = apply_swd_layout(fig_trend)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    with st.expander(f"Analysis for {trend_country}"):
        st.write(f"This chart reveals how dietary, lifestyle, or demographic changes over 30 years in {trend_country} impact specific cancers. For example, nations with rapid economic development often see Stomach cancer plateau while Colon/Rectum and Breast cancers rise sharply.")

st.divider()

st.markdown("### 3. Cancer Correlations Across Nations")
st.markdown("Investigate if high rates of one cancer correlate with high rates of another (e.g. lifestyle-related cancers).")
col5, col6, col7 = st.columns(3)
with col5:
    cancer_x = st.selectbox("X-Axis Cancer", df_countries['Cancer_Type'].unique(), index=list(df_countries['Cancer_Type'].unique()).index('Breast'))
with col6:
    cancer_y = st.selectbox("Y-Axis Cancer", df_countries['Cancer_Type'].unique(), index=list(df_countries['Cancer_Type'].unique()).index('Colon and rectum'))
with col7:
    corr_year = st.slider("Select Year", 1990, 2019, 2019, key="corr_year")

df_corr_year = df_countries[df_countries['Year'] == corr_year]
df_x = df_corr_year[df_corr_year['Cancer_Type'] == cancer_x][['Entity', 'Deaths']].rename(columns={'Deaths': cancer_x})
df_y = df_corr_year[df_corr_year['Cancer_Type'] == cancer_y][['Entity', 'Deaths']].rename(columns={'Deaths': cancer_y})
df_merged = df_x.merge(df_y, on='Entity').dropna()

fig_corr = px.scatter(df_merged, x=cancer_x, y=cancer_y, hover_name='Entity',
                      log_x=True, log_y=True,
                      title=f'Logarithmic Correlation: {cancer_x} vs {cancer_y} ({corr_year})',
                      labels={cancer_x: f'{cancer_x} (Log)', cancer_y: f'{cancer_y} (Log)'},
                      color_discrete_sequence=['#009E73'])
fig_corr = apply_swd_layout(fig_corr)
st.plotly_chart(fig_corr, use_container_width=True)
