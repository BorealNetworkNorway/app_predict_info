# app.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils import load_data, get_plot_coordinates, show_tree_map, get_tree_info

st.set_page_config(layout="wide", page_title="Forest Monitoring")
st.title("\ud83c\udf33 Forest Parcels Monitoring in Norway")

# Load data
data_by_plot = load_data("data/predict_tree_inventory_v3.xlsx")

# 1. Display map of Norway with forest parcel markers
st.header("\ud83d\uddfa Parcels in Norway")
map_center = [64.5, 11.0]
forest_map = folium.Map(location=map_center, zoom_start=5)

for plot_id, df in data_by_plot.items():
    loc = df["location"].iloc[0]
    coords = df["coordinates"].iloc[0]
    if coords:
        lat, lon = map(float, coords.split(","))
        folium.Marker(
            location=[lat, lon],
            tooltip=f"Plot {plot_id}: {loc}",
            popup=f"Click to view Plot {plot_id}"
        ).add_to(forest_map)

plot_selection = st_folium(forest_map, width=900, height=500)

# 2. User selects a plot manually or from the map
st.sidebar.title("\ud83d\udcc2 Select a Plot")
all_plots = list(data_by_plot.keys())
selected_plot = st.sidebar.selectbox("Choose a plot:", all_plots)
df_plot = data_by_plot[selected_plot]

# 3. Display tree distribution in the plot
st.subheader(f"\ud83c\udf33 Plot {selected_plot} - Tree Layout")
show_tree_map(df_plot)

# 4. Tree search bar
st.sidebar.title("\ud83d\udd0d Search Tree")
tree_id = st.sidebar.text_input("Enter tree_ID")
if tree_id:
    result = get_tree_info(df_plot, tree_id)
    st.sidebar.markdown("---")
    if result is not None:
        st.sidebar.write(result)
    else:
        st.sidebar.error("Tree not found")
