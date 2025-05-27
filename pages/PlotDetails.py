# PlotDetails.py

import streamlit as st
from utils import load_data, get_plot_metadata, show_tree_map, get_tree_info
import os
import folium
from PIL import Image
from streamlit_folium import st_folium

st.set_page_config(page_title="Plot Details", layout="wide")

if "selected_plot" not in st.session_state:
    st.error("No plot selected. Please go back to the home page.")
    st.stop()

plot_id = st.session_state["selected_plot"]
data_by_plot, metadata_df = load_data("data/predict_tree_inventory_v3.xlsx")
df_plot = data_by_plot[plot_id]
meta = get_plot_metadata(metadata_df, plot_id)

st.markdown(f"<h1 style='text-align: center;'>Welcome at plot {plot_id}</h1>", unsafe_allow_html=True)
st.subheader("Table complète des métadonnées des plots")
st.dataframe(metadata_df, use_container_width=True)
st.dataframe(meta, use_container_width=True)
st.write(plot_id)
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Plot {plot_id} information")
    st.markdown(f"**Location:** {meta.get('location', 'N/A')}")
    st.markdown(f"**Altitude:** {meta.get('altitude', 'N/A')}")
    st.markdown(f"**Access:** {meta.get('access', 'N/A')}")
    st.markdown(f"**Owner Contact:** {meta.get('owner_contact', 'N/A')}")
    st.markdown(f"**Number of Trees:** {meta.get('number_of_trees', 'N/A')}")
    st.markdown(f"**Category:** {meta.get('category', 'N/A')}")
    st.markdown(f"**County:** {meta.get('county', 'N/A')}")
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
    show_labels = st.checkbox("Tree IDs", value=False)
    show_dendro = st.checkbox("Show dendrometers and not drendrometers", value=True)
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
    st.sidebar.title("Search a tree")
    tree_id = st.sidebar.text_input("Enter tree_ID, pleaaaase")
    if tree_id:
        result = get_tree_info(df_plot, tree_id)
        st.sidebar.markdown("---")
        if result is not None:
            st.sidebar.write(result)
        else:
            st.sidebar.error("Tree not found")
with col2 : 
    if not dendros.empty:
        st.markdown("### Trees with Dendrometers")
        st.dataframe(dendros)
    else : 
        st.markdown("### Trees with Dendrometers")
        st.write(f"Il est l'heure de creuser le sol et d'installer une boite !")



image_path = f"data/images/{plot_id}.jpg"
if os.path.exists(image_path):
      image = Image.open(image_path)
      st.image(image, caption=f"Photo of plot {plot_id}", use_container_width=True)

st.button("Back to Home", on_click=lambda: st.switch_page("app.py"))
