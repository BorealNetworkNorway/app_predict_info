# utils.py
import pandas as pd
import altair as alt
import streamlit as st
import numpy as np

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
        st.warning("Certaines colonnes nécessaires sont manquantes.")
        return

    df = df.dropna(subset=["tree_id", "distance", "degrees"])
    df["x"] = df["distance"] * np.cos(df["degrees"] * np.pi / 200)
    df["y"] = df["distance"] * np.sin(df["degrees"] * np.pi / 200)

    # Déterminer une échelle carrée (même min/max pour x et y)
    min_x, max_x = df["x"].min(), df["x"].max()
    min_y, max_y = df["y"].min(), df["y"].max()
    min_val = min(min_x, min_y)
    max_val = max(max_x, max_y)

    # Appliquer le même domaine pour x et y
    x_axis = alt.X("x", scale=alt.Scale(domain=[min_val, max_val]))
    y_axis = alt.Y("y", scale=alt.Scale(domain=[min_val, max_val]))

    chart = alt.Chart(df).mark_circle().encode(
        x=x_axis,
        y=y_axis,
        tooltip=["tree_id", "species", "mean_dbh"],
        size=alt.Size("mean_dbh", scale=alt.Scale(range=[30, 200])),
        color=alt.Color("species:N")
    ).properties(
        width=500,
        height=500
    )

    st.altair_chart(chart, use_container_width=False)


def get_tree_info(df, tree_id):
    match = df[df["tree_id"].astype(str) == tree_id]
    if not match.empty:
        return match.iloc[0].to_frame().rename(columns={0: "value"})
    return None
