# --- utils.py ---

#Import
import pandas as pd
import streamlit as st
import numpy as np
import altair as alt


def load_data(excel_path):
    xls = pd.ExcelFile(excel_path)
    data_by_sheet = {}
    metadata_df = None

    for name in xls.sheet_names:
        df = xls.parse(name)
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

        if name == "metadata":
            metadata_df = df
        else:
            df["plot_id"] = name
            data_by_sheet[name] = df

    return data_by_sheet, metadata_df


def get_plot_coordinates(df):
    """
    Extract coordinates of a plot from the DataFrame
    """
    coords = df["coordinates"].iloc[0]
    if coords:
        return list(map(float, coords.split(",")))
    return None


def get_plot_metadata(metadata_df, plot_id):
    """
    Return metadata info for a specific plot_id
    """
    plot_row = metadata_df[metadata_df["plot_id"] == plot_id]
    st.dataframe(plot_row)
    first_row = metadata_df.iloc[0]
    metadata_dict = first_row.to_dict()
    
    if not plot_row.empty:
        return plot_row.to_dict()
    return {}


def show_tree_map(df, show_dendrometers=False, show_labels=False):
    """ 
    Display the map of the trees. 
    """

    # Ensure required columns are present (yeah I had a lot of errors) 
    if not {"tree_id", "mean_dbh", "distance", "degrees", "species"}.issubset(df.columns):
        st.warning("Some columns are missing.")
        return

    # Drop rows with missing elements
    df = df.dropna(subset=["tree_id", "distance", "degrees"])
    df = df.dropna(subset=["mean_dbh"])
    df["mean_dbh"] = pd.to_numeric(df["mean_dbh"], errors="coerce")

    # Convert coordinates : I divided by 200 cause the compas was with 400°. 
    df["x"] = df["distance"] * np.cos(df["degrees"] * np.pi / 200)
    df["y"] = df["distance"] * np.sin(df["degrees"] * np.pi / 200)
    
    df["has_dendrometer"] = df["dendrometer_id"].notna()
    # Dendrometer listing
    dendros = df[df["has_dendrometer"]][["tree_id", "dendrometer_id"]]

    
    # Base Altair chart setup with tooltips
    base = alt.Chart(df).encode(
        x=alt.X("x", scale=alt.Scale(domain=[-18, 18])),
        y=alt.Y("y", scale=alt.Scale(domain=[-18, 18])),
        tooltip=["tree_id", "species", "mean_dbh", "dendrometer_id"]
    )

    # Main layer: colored circles by species, sized by mean DBH
    if show_dendrometers:
        color_encoding = alt.condition(
            "datum.has_dendrometer",
            alt.value("orange"),
            alt.Color("species:N")
        )
    else:
        color_encoding = alt.Color("species:N")

    
    circles = base.mark_circle().encode(
        size=alt.Size("mean_dbh", scale=alt.Scale(range=[30, 200])),
        color=color_encoding
    )

    
    origin = alt.Chart(
        pd.DataFrame({'x': [0], 'y': [0]})
    ).mark_point(shape='cross',size=200,color='red').encode(
        x='x:Q', y='y:Q'
    )

    # Optional text labels for tree IDs
    if show_labels:
        text_layer = base.mark_text(align="center", dy=-10).encode(text="tree_id:N")
        chart = (circles + text_layer + origin)
    else:
        chart = (circles + origin)

    st.altair_chart(chart.properties(
                width = 800, height= 800,
                title=f"Plot probably full of rocks and roots"
    ).configure_legend(
        orient="right"
    ).interactive(), use_container_width=False)

    
def get_tree_info(df, tree_id):
    """
    Return information about a specific tree given its ID
    """
    match = df[df["tree_id"].astype(str) == tree_id]
    if not match.empty:
        return match.iloc[0].to_frame().rename(columns={0: "value"})
    return None
