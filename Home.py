import streamlit as st
from utils import load_data

st.set_page_config(page_title="Forest Explorer", layout="centered")

st.markdown("<h1 style='text-align: center;'>Forest PLots Explorer</h1>", unsafe_allow_html=True)

data_by_plot, metadata_df = load_data("data/predict_tree_inventory_v3.xlsx")
plot_ids = list(data_by_plot.keys())

selected_plot = st.selectbox("Choose a plot", plot_ids)

if st.button("View Plot Details"):
    st.session_state["selected_plot"] = selected_plot
    st.switch_page("pages/PlotDetails.py")
