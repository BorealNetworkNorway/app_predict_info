# --- app.py ---

#Import
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image
import os
from utils import load_data, get_plot_metadata, show_tree_map, get_tree_info

# page config
st.set_page_config(layout="wide", page_title="Predict Project")
st.markdown("""
    <style>
    /* Hide Streamlit footer and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header styling */
    h1 {
        color: 'white';
        font-size: 2.8em;
        font-weight: 600;
        border-bottom: 2px solid #81c784;
        padding-bottom: 0.3em;
        margin-bottom: 1em;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    .stButton>button {
        background-color: #4caf50;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        font-weight: bold;
    }

    .stDownloadButton>button {
        background-color: #00897b;
        color: white;
        border-radius: 8px;
        font-weight: 600;
    }

    .stDataFrame {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
    }

    .stImage {
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    }

    .stSidebar {
        background-color: #e0f2f1;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>Forest Plots Explorer</h1>", unsafe_allow_html=True)


#####################################################
# Load data (here you can change the name of the sheet.)
#####################################################
excel_path = "data/predict_tree_inventory_final.xlsx"
data_by_plot, metadata_df = load_data(excel_path)
plot_ids = list(data_by_plot.keys())

#Choice of the plot 

st.markdown("<h2 style='text-align:center;'>Choose a Plot</h2>", unsafe_allow_html=True)
centered_box = """
    <style>
    div[data-baseweb="select"] {
        margin-left: auto;
        margin-right: auto;
        width: 300px;
    }
    </style>
"""
st.markdown(centered_box, unsafe_allow_html=True)
selected_plot = st.selectbox("", plot_ids, label_visibility="collapsed")


if selected_plot not in data_by_plot:
        st.error("Plot not found, sorryyyy.")
        st.stop()
    
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("View Plot Details"):
        st.session_state["selected_plot"] = selected_plot
        st.switch_page("pages/PlotDetails.py")

#Map of Norway
st.header("Map of the plots in Norway")
map_center = [62.4, 11.0]
norway_map = folium.Map(location=map_center, zoom_start=6)
    
# Add one marker per plot 
for plot_id, df in data_by_plot.items():
    loc = df["location"].iloc[0]
    coords = df["coordinates"].iloc[0]
    if coords:
        lat, lon = map(float, coords.split(",")) # convert the coordinates to float
        folium.map.Marker(
            [lat, lon],
            icon=folium.DivIcon(
                html=f"""
                <div style="font-size: 9px; font-weight: bold; color: white;
                background-color: purple; border-radius: 4px;
                padding: 4px 5px; text-align: left; position: relative; left: -4px;">
                    {plot_id}
                 </div>
                    """
            ),
            tooltip=f"Plot {plot_id}: {loc}"
            ).add_to(norway_map)

# Display the folium map
map_response = st_folium(norway_map,  use_container_width=True, height=600)


    




