# PlotDetails.py

import streamlit as st
from utils import load_data, get_plot_metadata, show_tree_map, get_tree_info, get_species_composition
import os
import folium
from PIL import Image
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(page_title="Plot Details", layout="wide")

if "selected_plot" not in st.session_state:
    st.error("No plot selected. Please go back to the home page.")
    st.stop()

plot_id = st.session_state["selected_plot"]
data_by_plot, metadata_df = load_data("data/predict_tree_inventory_final.xlsx")
df_plot = data_by_plot[plot_id]
meta = get_plot_metadata(metadata_df, plot_id)

st.markdown(f"<h1 style='text-align: center;'>Welcome at plot {plot_id}</h1>", unsafe_allow_html=True)
st.markdown(f"**Comments :** {meta.get('comments', 'N/A')}")

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Plot {plot_id} information")
    st.markdown(f"**Location:** {meta.get('location', 'N/A')}")
    st.markdown(f"**County:** {meta.get('county', 'N/A')}")
    st.markdown(f"**Category:** {meta.get('category', 'N/A')}")
    st.markdown(f"**Owner Contact:** {meta.get('owner_contact', 'N/A')}")
    st.markdown(f"**Access:** {meta.get('access', 'N/A')}")
    st.markdown(f"**Number of Trees:** {meta.get('number_of_trees', 'N/A')}")
    st.markdown(f"**Altitude (m):** {meta.get('altitude', 'N/A')}")
    st.markdown(f"**Mean temperature (°C):** {meta.get('mean_temperature', 'N/A')}")
    st.markdown(f"**Annual precipitation (mm):** {meta.get('mean_precipitation', 'N/A')}")
    st.markdown(f"**Main rock:** {meta.get('geology', 'N/A')}")
    st.markdown(f"**Soil type:** {meta.get('pedology', 'N/A')}")
    st.markdown(f"**Box Number:** {meta.get('box_number', 'N/A')}")

with col2:

    coords = df_plot["coordinates"].iloc[0]
    if coords:
        lat, lon = map(float, coords.split(","))
        local_map = folium.Map(location=[lat, lon], zoom_start=14)
        folium.Marker([lat, lon], tooltip=f"Plot {plot_id}").add_to(local_map)
        st_folium(local_map, width=800, height=400)

    

#####################################################
# Plot display options
#####################################################
with st.expander("Plot View Options", expanded=True):
    show_labels = st.checkbox("Tree IDs", value=True)
    show_dendro = st.checkbox("Show dendrometers and not drendrometers (in orange)", value=False)
    st.download_button("Download plot as csv", data=df_plot.to_csv(index=False), file_name=f"plot_{plot_id}.csv")


#####################################################
# Tree map 
####################################################

title_tree_map = f"Plot {plot_id} ({df_plot['location'].iloc[0]})"
st.subheader(title_tree_map)

show_tree_map(df_plot, show_dendrometers=show_dendro, show_labels=show_labels)

#####################################################
# Search for a specific tree in the sidebar / display dendrometer tress
#####################################################
col1, col2 = st.columns(2)
with col1 :
    
    st.subheader("Species composition")
    df_plot = data_by_plot[plot_id]
    species_composition_df = get_species_composition(df_plot)
    
    if not species_composition_df.empty:
        # Définir les couleurs personnalisées
        color_map = {
            's': 'green',   # spruce
            'p': 'orange',  # pine
            # Couleurs par défaut pour d'autres espèces
        }
    
        # Ajouter des couleurs aléatoires pour les espèces non définies
        default_colors = px.colors.qualitative.Pastel + px.colors.qualitative.Bold
        for species in species_composition_df["Species"]:
            if species not in color_map:
                color_map[species] = default_colors.pop(0)
    
        # Création du graphique
        fig = px.pie(
            species_composition_df,
            names="Species",
            values="Percentage",
            title="Tree Species Composition (%)",
            color="Species",
            color_discrete_map=color_map
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No species data available for this plot.")

    st.markdown("---")
    st.title("Search a tree")
    tree_id = st.text_input("Enter tree_ID, pleaaaase")
    if tree_id:
        result = get_tree_info(df_plot, tree_id)
        st.markdown("---")
        if result is not None:
            st.write(result)
        else:
            st.error("Tree not found")
with col2 : 
    df_plot["has_dendrometer"] = df_plot["dendrometer_id"].notna()
    dendro_df = df_plot[df_plot["has_dendrometer"]][["tree_id", "dendrometer_id"]].dropna()
    st.markdown("#### Trees with Dendrometers")
    if not dendro_df.empty : 
        st.dataframe(dendro_df)
    else : 
        st.write(f"Il est l'heure de creuser le sol et d'installer une boite !")

    
    

image_path = f"data/images/{plot_id}.jpg"
if os.path.exists(image_path):
      image = Image.open(image_path)
      st.image(image, caption=f"Photo of plot {plot_id}", use_container_width=True)
image_path_2 = f"data/images/{plot_id}.png"
if os.path.exists(image_path):
      image = Image.open(image_path)
      st.image(image, caption=f"Photo of plot {plot_id}", use_container_width=True)

