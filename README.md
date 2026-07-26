# Global Cancer Trends Dashboard 🌍🩺

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An interactive, multi-dimensional analysis of global cancer mortality (1990-2019) using Plotly and Streamlit.

## 📖 Overview
This project explores 30 years of global cancer mortality data from the **Institute for Health Metrics and Evaluation (IHME)**. It features a deep-dive Exploratory Data Analysis (EDA) Jupyter Notebook answering 10+ analytical questions, and a highly polished interactive Streamlit dashboard.

The visualizations strictly adhere to **Storytelling with Data (SWD)** and publication-ready design principles:
- **Color Vision Deficiency (CVD)** safe palettes.
- Decluttered charts (no gridlines or chart junk).
- Direct annotations and insights as titles.

## 📂 Project Structure
- `data/` - Contains the raw CSV data sourced from Our World in Data / IHME.
- `notebooks/` - Contains the `analysis_notebook.ipynb` with 10 analytical questions and Plotly charts.
- `app.py` - The entry point for the Streamlit dashboard.
- `pages/` - Sub-pages for the multi-tab interactive dashboard.
- `presentation.pdf` - The final slide deck summarizing key insights.

## 🚀 How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/global-cancer-dashboard.git
   cd global-cancer-dashboard
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit Dashboard:
   ```bash
   streamlit run app.py
   ```

## 📊 Dataset
Source: [Our World in Data (IHME Global Burden of Disease)](https://ourworldindata.org/cancer)

## 🏆 Deliverables for Course
This repository fulfills the requirements for the Data Visualization Final Individual Project (Summer 2026).
