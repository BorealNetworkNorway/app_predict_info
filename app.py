# app.py

#Import
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils import load_data, get_plot_coordinates, show_tree_map, get_tree_info

st.set_page_config(layout="wide", page_title="Forest Monitoring")
st.title("Predict Project - Forest Plots")

# Load data
data_by_plot = load_data("data/predict_tree_inventory_v3.xlsx")

#####################################################
# 1. Display map of Norway with forest parcel markers 
#####################################################
st.header("Map of the plots in Norway")
map_center = [64.5, 11.0]
forest_map = folium.Map(location=map_center, zoom_start=5)

for plot_id, df in data_by_plot.items():
    loc = df["location"].iloc[0]
    coords = df["coordinates"].iloc[0]
    if coords:
        lat, lon = map(float, coords.split(","))
        color = "blue"
        folium.Marker(
            location=[lat, lon],
            tooltip=f"Plot {plot_id}: {loc}",
            popup=f"Click to view plot {plot_id}",
            icon=folium.Icon(color=color)
        ).add_to(forest_map)
       

map_response = st_folium(forest_map, width=1000, height=600)


st.sidebar.title("Select a Plot")
# Dropdown visible en permanence
all_plots = list(data_by_plot.keys())
dropdown_plot = st.sidebar.selectbox("Choose a plot manually:", all_plots)

# If click on the map : 
clicked_plot = None
if map_response.get("last_object_clicked_tooltip"):
    tooltip = map_response["last_object_clicked_tooltip"]
    try:
        clicked_plot = tooltip.split()[1]
        if clicked_plot not in all_plots:
            clicked_plot = None
    except:
        clicked_plot = None

# Final choice
selected_plot = clicked_plot if clicked_plot else dropdown_plot

# Making sure that the key exists
if selected_plot not in data_by_plot:
    st.error(f"Selected plot '{selected_plot}' not found in data.")
    st.stop()

for plot_id, df in data_by_plot.items():
    loc = df["location"].iloc[0]
    coords = df["coordinates"].iloc[0]
    if coords:
        lat, lon = map(float, coords.split(","))
            
        # If plot selected, draw it in red 
        if plot_id == selected_plot: 
            color = "red" 

            folium.Marker(
                location=[lat, lon],
                tooltip=f"Plot {plot_id}: {loc}",
                popup=f"Click to view plot {plot_id}",
                icon=folium.Icon(color=color)
            ).add_to(forest_map)
       

# Data loading
df_plot = data_by_plot[selected_plot]



dendro_trees = df_plot[df_plot.get("dendrometer_id").notna()]["tree_id"].tolist()
if dendro_trees:
    st.sidebar.markdown(f"**Dendrometer trees :** ")
    st.sidebar.markdown(f"{', '.join(map(str, dendro_trees))}")
else:
    st.sidebar.markdown("*No dendrometers recorded for now :(*")


# Options
with st.expander("Plot View Options", expanded=True):
    show_labels = st.checkbox("Tree IDs", value=False)
    st.download_button("Download plot as csv", data=df_plot.to_csv(index=False), file_name=f"plot_{selected_plot}.csv")


# Display plot
title = f"Plot {selected_plot} - Tree Layout -  ({df_plot['location'].iloc[0]})"
st.subheader(title)
show_tree_map(df_plot, show_labels=show_labels)

# 4. Tree search bar
st.sidebar.title("Search Tree")
tree_id = st.sidebar.text_input("Enter tree_ID, pleaaaase")
if tree_id:
    result = get_tree_info(df_plot, tree_id)
    st.sidebar.markdown("---")
    if result is not None:
        st.sidebar.write(result)
    else:
        st.sidebar.error("Tree not found")
