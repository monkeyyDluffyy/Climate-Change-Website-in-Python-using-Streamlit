import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
import zipfile
import requests

# Set up Streamlit page
st.set_page_config(page_title="🌍 Climate Indicators Dashboard", layout="wide")
st.title("🌍 Global Climate & Environmental Indicators")

# File & folder paths
shapefile_url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip"
zip_path = "data/natural_earth/ne_110m_admin_0_countries.zip"
shapefile_dir = "data/natural_earth"
shapefile_path = os.path.join(shapefile_dir, "ne_110m_admin_0_countries.shp")

# Download & extract shapefile if needed
def download_and_extract_shapefile():
    if not os.path.exists(shapefile_path):
        os.makedirs(shapefile_dir, exist_ok=True)
        st.info("Downloading shapefile...")
        response = requests.get(shapefile_url)
        with open(zip_path, "wb") as f:
            f.write(response.content)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(shapefile_dir)
        st.success("Shapefile downloaded and extracted!")

# Load shapefile into GeoDataFrame
@st.cache_data
def load_world():
    download_and_extract_shapefile()
    return gpd.read_file(shapefile_path)

# Simulated environmental data
@st.cache_data
def load_data():
    data = {
        'iso_a3': ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'AUS', 'CAN', 'ZAF', 'GBR', 'FRA'],
        'sea_level_rise_mm': [3.2, 2.5, 2.8, 2.9, 2.7, 3.0, 3.1, 2.4, 2.6, 2.5],
        'heat_wave_days': [15, 30, 35, 25, 10, 20, 12, 28, 14, 16],
        'aqi': [90, 150, 160, 120, 100, 80, 70, 130, 60, 65],
        'temp_change_C': [1.1, 1.4, 1.2, 1.3, 1.0, 1.5, 1.3, 1.1, 1.2, 1.1]
    }
    return pd.DataFrame(data)

# Load world map and merge with data
world = load_world()
env_df = load_data()
world = world.merge(env_df, on='iso_a3', how='left')

# Dropdown for indicators
indicator_options = {
    'sea_level_rise_mm': '🌊 Sea Level Rise (mm)',
    'heat_wave_days': '🔥 Heat Wave Days',
    'aqi': '💨 Air Quality Index (AQI)',
    'temp_change_C': '🌡 Global Temperature Change (°C)'
}

indicator = st.selectbox("Select Indicator to Visualize:", list(indicator_options.keys()), format_func=lambda x: indicator_options[x])

# Plot
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
world.plot(
    column=indicator,
    ax=ax,
    legend=True,
    cmap='coolwarm',
    missing_kwds={
        "color": "lightgrey",
        "label": "No data"
    }
)
ax.set_title(indicator_options[indicator], fontsize=18)
ax.axis('off')
st.pyplot(fig)
