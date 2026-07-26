import streamlit as st
import plotly.express as px
from utils import load_data, apply_swd_layout

st.title("Demographic & Regional Shifts")
st.markdown("Compare cancer burdens between aging and younger populations across different regions.")

df = load_data()

st.subheader("Breast vs. Cervical Cancer Burden")
regions_q3 = ['United States', 'Nigeria', 'India', 'Germany', 'Brazil']
df_q3 = df[(df['Entity'].isin(regions_q3)) & 
           (df['Cancer_Type'].isin(['Breast', 'Cervical'])) & 
           (df['Year'] == 2019)]

fig3 = px.bar(df_q3, x='Deaths', y='Entity', color='Cancer_Type', orientation='h',
              title='In Nigeria and India, Cervical cancer deaths rival or exceed Breast cancer deaths',
              color_discrete_map={'Breast': '#CC79A7', 'Cervical': '#E69F00'}, barmode='group')

fig3 = apply_swd_layout(fig3)
fig3.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig3, use_container_width=True)
