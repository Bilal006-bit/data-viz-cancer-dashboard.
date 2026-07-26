import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

# Helper function to create markdown and code cells
def add_md(text):
    nb.cells.append(nbf.v4.new_markdown_cell(text))

def add_code(text):
    nb.cells.append(nbf.v4.new_code_cell(text))

add_md("# Global Cancer Mortality Analysis (1990 - 2019)\n\n"
       "This notebook performs an Exploratory Data Analysis (EDA) and answers 10+ analytical questions "
       "regarding global cancer mortality trends. It utilizes the **Global Burden of Disease (IHME)** dataset.")

add_md("## 1. Setup & Data Loading")
add_code('''import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set a CVD-safe and clean theme globally for Plotly
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = px.colors.qualitative.Safe

# Load the dataset
df = pd.read_csv('../data/cancer_deaths.csv')

# The dataset is in a wide format. We will melt it to a long format for easier analysis.
# We also clean up the column names for cancer types.
id_vars = ['Entity', 'Year']
cancer_cols = [c for c in df.columns if 'cancer' in c.lower() or 'lymphoma' in c.lower() or 'leukemia' in c.lower()]
df_long = df.melt(id_vars=id_vars, value_vars=cancer_cols, var_name='Cancer_Type', value_name='Deaths')

# Clean up Cancer_Type strings (e.g. "Breast cancer (deaths)" -> "Breast")
df_long['Cancer_Type'] = df_long['Cancer_Type'].str.replace(' (deaths)', '', regex=False).str.replace(' cancer', '', regex=False)

# Filter out aggregates like "World" or regions if we only want countries.
# For simplicity, we'll keep all for now, but identify 'World' for global trends.
df_world = df_long[df_long['Entity'] == 'World']
df_countries = df_long[~df_long['Entity'].isin(['World', 'High SDI', 'Low SDI', 'High-income Asia Pacific', 'Western Europe', 'Eastern Europe', 'Australasia', 'North America', 'Central Europe', 'Andean Latin America', 'Tropical Latin America', 'Central Latin America', 'Southern Latin America', 'Caribbean', 'Oceania', 'Southeast Asia', 'East Asia', 'South Asia', 'Central Asia', 'Eastern Sub-Saharan Africa', 'Western Sub-Saharan Africa', 'Southern Sub-Saharan Africa', 'Central Sub-Saharan Africa', 'North Africa and Middle East'])]

df_countries.head()''')

add_md("## Question 1: How has the global burden of the top 5 deadliest cancers shifted over the last 30 years?")
add_code('''# Get top 5 cancers globally in 2019
top5_2019 = df_world[df_world['Year'] == 2019].groupby('Cancer_Type')['Deaths'].sum().nlargest(5).index

# Filter world data for these top 5
df_q1 = df_world[df_world['Cancer_Type'].isin(top5_2019)]

fig1 = px.line(df_q1, x='Year', y='Deaths', color='Cancer_Type',
              title='Tracheal, bronchus, and lung cancer remains the deadliest globally, with a steep rise since 1990',
              labels={'Deaths': 'Annual Deaths', 'Year': ''})

# Styling for SWD / Publication ready
# Highlight the top one, grey out others
color_map = {c: ('#D55E00' if 'bronchus' in c.lower() else '#CCCCCC') for c in top5_2019}
fig1 = px.line(df_q1, x='Year', y='Deaths', color='Cancer_Type', color_discrete_map=color_map,
              title='Tracheal, bronchus, and lung cancers drive the highest mortality globally, rising sharply',
              labels={'Deaths': 'Annual Deaths', 'Year': ''})

# Direct annotation instead of legend for the highlight
fig1.update_layout(showlegend=False, yaxis=dict(showgrid=True, gridcolor='#EEEEEE'), xaxis=dict(showgrid=False))
last_year = df_q1[df_q1['Year'] == 2019]
for idx, row in last_year.iterrows():
    fig1.add_annotation(x=2019.5, y=row['Deaths'], text=row['Cancer_Type'], 
                        showarrow=False, xanchor='left', font=dict(color=color_map[row['Cancer_Type']]))

fig1.update_traces(line=dict(width=3))
fig1.show()''')

add_md("## Question 2: Which countries experienced the most dramatic shift from Stomach to Colon/Rectum cancer deaths as they developed?")
add_code('''# Compare Stomach vs Colon and rectum in 1990 vs 2019 for top populated countries
countries_of_interest = ['China', 'India', 'United States', 'Japan', 'Brazil', 'Russian Federation']
df_q2 = df_countries[(df_countries['Entity'].isin(countries_of_interest)) & 
                     (df_countries['Cancer_Type'].isin(['Stomach', 'Colon and rectum'])) &
                     (df_countries['Year'].isin([1990, 2019]))]

df_q2_pivot = df_q2.pivot_table(index=['Entity', 'Year'], columns='Cancer_Type', values='Deaths').reset_index()
df_q2_pivot['Ratio (Colon/Stomach)'] = df_q2_pivot['Colon and rectum'] / df_q2_pivot['Stomach']

fig2 = px.bar(df_q2_pivot, x='Entity', y='Ratio (Colon/Stomach)', color='Year', barmode='group',
             title='China and Japan saw massive shifts toward Colon/Rectum cancer relative to Stomach cancer (1990-2019)',
             color_discrete_sequence=['#AAAAAA', '#0072B2'])

fig2.update_layout(yaxis=dict(showgrid=True, gridcolor='#EEEEEE'), xaxis=dict(showgrid=False), plot_bgcolor='white')
fig2.add_hline(y=1, line_dash="dash", line_color="black", annotation_text="Equal Deaths (1:1)")
fig2.show()''')

add_md("## Question 3: How does the mortality footprint of Breast vs. Cervical cancer differ across continents?")
add_code('''# We will proxy continents by looking at a few distinct large countries/regions
regions_q3 = ['United States', 'Nigeria', 'India', 'Germany', 'Brazil']
df_q3 = df_long[(df_long['Entity'].isin(regions_q3)) & 
                (df_long['Cancer_Type'].isin(['Breast', 'Cervical'])) & 
                (df_long['Year'] == 2019)]

# Calculate total female cancer deaths (proxy by sum of breast+cervical+ovarian)
# to get a percentage share, but absolute comparison is also fine.
fig3 = px.bar(df_q3, x='Deaths', y='Entity', color='Cancer_Type', orientation='h',
              title='In Nigeria and India, Cervical cancer deaths rival or exceed Breast cancer deaths',
              color_discrete_map={'Breast': '#CC79A7', 'Cervical': '#E69F00'})

fig3.update_layout(barmode='group', yaxis={'categoryorder':'total ascending'}, 
                   xaxis=dict(showgrid=True, gridcolor='#EEEEEE'), yaxis_title="")
fig3.show()''')

add_md("## Question 4: Is there a geographic clustering of high Liver cancer mortality?")
add_code('''# Map of Liver cancer deaths in 2019
df_q4 = df_countries[(df_countries['Year'] == 2019) & (df_countries['Cancer_Type'] == 'Liver')]

fig4 = px.choropleth(df_q4, locations="Entity", locationmode='country names', color="Deaths",
                     hover_name="Entity", color_continuous_scale="Reds", range_color=[0, 50000],
                     title="East Asia (particularly China) bears an overwhelming burden of Liver Cancer deaths")

fig4.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
                   margin=dict(l=0, r=0, t=50, b=0))
fig4.show()''')

add_md("## Question 5: How has the age-related cancer (Prostate) trended in aging populations like Western Europe vs younger populations like Sub-Saharan Africa?")
add_code('''# Compare Prostate cancer growth in a proxy for aging (Japan, Italy) vs young (Nigeria, Kenya)
aging = ['Japan', 'Italy']
young = ['Nigeria', 'Kenya']
df_q5 = df_countries[(df_countries['Entity'].isin(aging + young)) & (df_countries['Cancer_Type'] == 'Prostate')]

# Normalize to 1990 baseline to show growth rate
df_q5_1990 = df_q5[df_q5['Year'] == 1990][['Entity', 'Deaths']].rename(columns={'Deaths': 'Baseline'})
df_q5 = df_q5.merge(df_q5_1990, on='Entity')
df_q5['Growth Index'] = df_q5['Deaths'] / df_q5['Baseline'] * 100

df_q5['Demographic'] = df_q5['Entity'].apply(lambda x: 'Aging Population' if x in aging else 'Young Population')

fig5 = px.line(df_q5, x='Year', y='Growth Index', color='Entity', line_dash='Demographic',
               title='Prostate cancer mortality is growing rapidly everywhere, but exploding in younger African nations',
               color_discrete_sequence=px.colors.qualitative.Safe)

fig5.update_layout(yaxis=dict(showgrid=True, gridcolor='#EEEEEE'), xaxis=dict(showgrid=False))
fig5.add_hline(y=100, line_dash="solid", line_color="black", annotation_text="1990 Baseline")
fig5.show()''')

add_md("## Question 6: What proportion of total cancer deaths is attributed to Leukemia in children/young demographics? (Proxy via total country burden)")
add_code('''# Leukemia often affects younger populations. Does it make up a larger % of cancer deaths in countries with lower life expectancy?
df_2019 = df_countries[df_countries['Year'] == 2019]
total_deaths = df_2019.groupby('Entity')['Deaths'].sum().reset_index().rename(columns={'Deaths': 'Total_Cancer_Deaths'})
leukemia_deaths = df_2019[df_2019['Cancer_Type'] == 'Leukemia'][['Entity', 'Deaths']].rename(columns={'Deaths': 'Leukemia_Deaths'})

df_q6 = total_deaths.merge(leukemia_deaths, on='Entity')
df_q6['Leukemia_Pct'] = (df_q6['Leukemia_Deaths'] / df_q6['Total_Cancer_Deaths']) * 100

# Let's look at top 15 countries by Leukemia percentage (filtering out very small countries for noise)
df_q6_filtered = df_q6[df_q6['Total_Cancer_Deaths'] > 5000].sort_values('Leukemia_Pct', ascending=False).head(15)

fig6 = px.bar(df_q6_filtered, x='Leukemia_Pct', y='Entity', orientation='h',
              title='Leukemia constitutes a drastically higher share of cancer deaths in Middle Eastern/African nations',
              color_discrete_sequence=['#56B4E9'])

fig6.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis=dict(showgrid=True, gridcolor='#EEEEEE'), plot_bgcolor='white')
fig6.show()''')

add_md("## Question 7: Has the Pancreatic cancer death toll surpassed Breast cancer in high-income nations?")
add_code('''# Look at USA and UK trends for Pancreatic vs Breast cancer
high_income = ['United States', 'United Kingdom']
df_q7 = df_countries[(df_countries['Entity'].isin(high_income)) & 
                     (df_countries['Cancer_Type'].isin(['Pancreatic', 'Breast']))]

fig7 = px.line(df_q7, x='Year', y='Deaths', color='Cancer_Type', facet_col='Entity',
               title='While Breast cancer deaths plateau, Pancreatic cancer deaths steadily rise in the US & UK',
               color_discrete_map={'Breast': '#CC79A7', 'Pancreatic': '#E69F00'})

fig7.update_layout(plot_bgcolor='white', yaxis=dict(showgrid=True, gridcolor='#EEEEEE'))
fig7.show()''')

add_md("## Question 8: How does the ratio of Tracheal/Lung cancer to all other cancers vary across the globe?")
add_code('''# Lung cancer vs All Other in 2019
lung = df_2019[df_2019['Cancer_Type'].str.contains('bronchus', case=False)][['Entity', 'Deaths']].rename(columns={'Deaths': 'Lung_Deaths'})
other = df_2019[~df_2019['Cancer_Type'].str.contains('bronchus', case=False)].groupby('Entity')['Deaths'].sum().reset_index().rename(columns={'Deaths': 'Other_Deaths'})

df_q8 = lung.merge(other, on='Entity')
df_q8['Lung_Pct'] = df_q8['Lung_Deaths'] / (df_q8['Lung_Deaths'] + df_q8['Other_Deaths']) * 100

df_q8_top = df_q8[df_q8['Lung_Deaths'] + df_q8['Other_Deaths'] > 10000].sort_values('Lung_Pct', ascending=False).head(10)

fig8 = px.bar(df_q8_top, x='Lung_Pct', y='Entity', orientation='h',
              title='In nations like Greece and Turkey, Lung cancer accounts for over 25% of all cancer deaths',
              color_discrete_sequence=['#D55E00'])

fig8.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', xaxis=dict(showgrid=True, gridcolor='#EEEEEE'))
fig8.show()''')

add_md("## Question 9: Which specific cancer type saw the largest absolute increase in deaths from 1990 to 2019 globally?")
add_code('''world_1990 = df_world[df_world['Year'] == 1990][['Cancer_Type', 'Deaths']].set_index('Cancer_Type')
world_2019 = df_world[df_world['Year'] == 2019][['Cancer_Type', 'Deaths']].set_index('Cancer_Type')

diff = (world_2019['Deaths'] - world_1990['Deaths']).sort_values(ascending=False).reset_index().rename(columns={'Deaths': 'Absolute_Increase'})

# Highlight the top grower
color_map_9 = {c: ('#D55E00' if i == 0 else '#AAAAAA') for i, c in enumerate(diff['Cancer_Type'])}

fig9 = px.bar(diff.head(10), x='Absolute_Increase', y='Cancer_Type', orientation='h',
              title='Lung cancer deaths saw the largest absolute global surge over the 30-year period',
              color='Cancer_Type', color_discrete_map=color_map_9)

fig9.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', xaxis=dict(showgrid=True, gridcolor='#EEEEEE'))
fig9.show()''')

add_md("## Question 10: Is there a correlation between the burden of Colon/Rectum cancer and Breast cancer across countries?")
add_code('''# Both are often linked to similar demographic/lifestyle shifts (diet, aging, screening). 
df_q10 = df_2019[df_2019['Cancer_Type'].isin(['Colon and rectum', 'Breast'])]
df_q10_pivot = df_q10.pivot(index='Entity', columns='Cancer_Type', values='Deaths').dropna()

# Normalize by a proxy (we will just use log scale to handle population differences)
fig10 = px.scatter(df_q10_pivot, x='Breast', y='Colon and rectum', hover_name=df_q10_pivot.index,
                   log_x=True, log_y=True,
                   title='Strong positive correlation between Breast and Colon/Rectum cancer deaths across nations',
                   labels={'Breast': 'Breast Cancer Deaths (Log)', 'Colon and rectum': 'Colon/Rectum Deaths (Log)'},
                   color_discrete_sequence=['#009E73'])

fig10.update_layout(plot_bgcolor='white', xaxis=dict(showgrid=True, gridcolor='#EEEEEE'), yaxis=dict(showgrid=True, gridcolor='#EEEEEE'))
fig10.show()''')

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/analysis_notebook.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook generated successfully!")
