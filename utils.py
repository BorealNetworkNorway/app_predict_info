# utils.py

#Import
import pandas as pd
import altair as alt
import streamlit as st
import numpy as np
import io 
import base64

#Loading of data 
def load_data(excel_path):
    xls = pd.ExcelFile(excel_path)
    data_by_sheet = {}
    for name in xls.sheet_names:
        df = xls.parse(name)
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        df["plot_id"] = name
        data_by_sheet[name] = df
    return data_by_sheet

def get_plot_coordinates(df):
    coords = df["coordinates"].iloc[0]
    if coords:
        return list(map(float, coords.split(",")))
    return None

def show_tree_map(df, show_dendrometers=False, show_labels=False):
    if not {"tree_id", "mean_dbh", "distance", "degrees", "species"}.issubset(df.columns):
        st.warning("Some columns are missing.")
        return

    df = df.dropna(subset=["tree_id", "distance", "degrees"])
    df = df.dropna(subset=["mean_dbh"])
    df["mean_dbh"] = pd.to_numeric(df["mean_dbh"], errors="coerce")
    
    df["x"] = df["distance"] * np.cos(df["degrees"] * np.pi / 200)
    df["y"] = df["distance"] * np.sin(df["degrees"] * np.pi / 200)
    #I divided by 200 cause the compas was with 400°. 
    
    
    
    base = alt.Chart(df).encode(
        x=alt.X("x", scale=alt.Scale(domain=[-18, 18])),
        y=alt.Y("y", scale=alt.Scale(domain=[-18, 18])),
        tooltip=["tree_id", "species", "mean_dbh", "dendrometer_id"]
    )

    species_layer = base.mark_circle().encode(
        size=alt.Size("mean_dbh", scale=alt.Scale(range=[30, 200])),
        color=alt.Color("species:N")
    )

    if show_labels:
        text_layer = base.mark_text(align="center", dy=-10).encode(text="tree_id:N")
        chart = (species_layer + text_layer).properties(
        width=1000, height=1000, title=f"Tree Layout - {df['location'].iloc[0]}"
    ).configure_legend(
        orient="right"
    ).interactive()
    else:
        chart = species_layer.properties(
        width=1000, height=1000, title=f"Tree Layout - {df['location'].iloc[0]}"
    ).configure_legend(
        orient="right"
    ).interactive()

    st.altair_chart(chart, use_container_width=False)

    download_link = get_chart_download_link(chart)
    if download_link:
        st.markdown(download_link, unsafe_allow_html=True)

def get_tree_info(df, tree_id):
    match = df[df["tree_id"].astype(str) == tree_id]
    if not match.empty:
        return match.iloc[0].to_frame().rename(columns={0: "value"})
    return None

def get_chart_download_link(chart, filename="chart.png"):
    try:
        import vl_convert as vlc
        img_bytes = vlc.vegalite_to_image(chart.to_dict(), format="png")
        b64 = base64.b64encode(img_bytes).decode()
        href = f'<a href="data:image/png;base64,{b64}" download="{filename}">📷 Télécharger l\'image</a>'
        return href
    except Exception as e:
        st.error(f"Erreur de génération d'image : {e}")
        return None
