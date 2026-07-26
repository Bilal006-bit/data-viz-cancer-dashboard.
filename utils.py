import pandas as pd
import streamlit as st
import plotly.express as px

# Set CVD-safe palette globally for all plots
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = px.colors.qualitative.Safe

@st.cache_data
def load_data():
    """Loads and melts the IHME cancer deaths dataset into long format."""
    df = pd.read_csv('data/cancer_deaths.csv')
    
    id_vars = ['Entity', 'Year']
    cancer_cols = [c for c in df.columns if 'cancer' in c.lower() or 'lymphoma' in c.lower() or 'leukemia' in c.lower()]
    df_long = df.melt(id_vars=id_vars, value_vars=cancer_cols, var_name='Cancer_Type', value_name='Deaths')
    
    # Clean cancer names
    df_long['Cancer_Type'] = df_long['Cancer_Type'].str.replace(' (deaths)', '', regex=False).str.replace(' cancer', '', regex=False)
    
    # Exclude aggregate regions to focus on specific countries/world
    exclude_list = ['High SDI', 'Low SDI', 'High-income Asia Pacific', 'Western Europe', 'Eastern Europe', 'Australasia', 'North America', 'Central Europe', 'Andean Latin America', 'Tropical Latin America', 'Central Latin America', 'Southern Latin America', 'Caribbean', 'Oceania', 'Southeast Asia', 'East Asia', 'South Asia', 'Central Asia', 'Eastern Sub-Saharan Africa', 'Western Sub-Saharan Africa', 'Southern Sub-Saharan Africa', 'Central Sub-Saharan Africa', 'North Africa and Middle East']
    return df_long[~df_long['Entity'].isin(exclude_list)]

def apply_swd_layout(fig):
    """Applies Storytelling with Data (SWD) layout rules to a Plotly figure."""
    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE', title=""),
        margin=dict(t=50, l=0, r=0, b=0)
    )
    return fig
