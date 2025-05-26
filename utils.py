# utils.py

#Import
import pandas as pd
import altair as alt
import streamlit as st
import numpy as np

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

def show_tree_map(df):
    if not {"tree_id", "mean_dbh", "distance", "degrees", "species"}.issubset(df.columns):
        st.warning("Some columns are missing.")
        return

    df = df.dropna(subset=["tree_id", "distance", "degrees"])
    df["x"] = df["distance"] * np.cos(df["degrees"] * np.pi / 200)
    df["y"] = df["distance"] * np.sin(df["degrees"] * np.pi / 200)
    #I divided by 200 cause the compas was with 400°. 

    df["has_dendrometer"] = df["dendrometer_id"].notna()

    
    base = alt.Chart(df).encode(
        x=alt.X("x", scale=alt.Scale(domain=[-20, 20])),
        y=alt.Y("y", scale=alt.Scale(domain=[-20, 20])),
        tooltip=["tree_id", "species", "mean_dbh", "dendrometer_id"]
    )

    species_layer = base.mark_circle().encode(
        size=alt.Size("mean_dbh", scale=alt.Scale(range=[30, 200])),
        color=alt.condition(
            show_dendrometers,
            alt.condition("datum.has_dendrometer", alt.value("orange"), alt.Color("species:N")),
            alt.Color("species:N")
        )
    )

    text_layer = base.mark_text(align="center", dy=-10).encode(
        text="tree_id:N"
    ) if show_labels else alt.Chart(pd.DataFrame())

    chart = (species_layer + text_layer).properties(
        width=600, height=600, title=f"Tree Layout - {df['location'].iloc[0]}"
    ).configure_legend(
        orient="right"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    # Dendrometer listing
    dendros = df[df["has_dendrometer"]][["tree_id", "dendrometer_id"]]
    if not dendros.empty:
        st.markdown("### Trees with Dendrometers")
        st.dataframe(dendros)

def get_tree_info(df, tree_id):
    match = df[df["tree_id"].astype(str) == tree_id]
    if not match.empty:
        return match.iloc[0].to_frame().rename(columns={0: "value"})
    return None
