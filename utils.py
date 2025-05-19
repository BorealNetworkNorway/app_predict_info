# utils.py
import pandas as pd
import altair as alt
import streamlit as st

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
    df["x"] = df["distance"] * np.cos(df["degrees"]*PI()/200)
    df["y"] = df["distance"] * np.sin(df["degrees"]*PI()/200)

    chart = alt.Chart(df).mark_circle().encode(
        x="x", y="y", tooltip=["tree_id", "species", "mean_dbh"],
        size=alt.Size("mean_dbh", scale=alt.Scale(range=[30, 200])),
        color=alt.Color("species:N")
    ).interactive().properties(width=700, height=500)

    st.altair_chart(chart)

def get_tree_info(df, tree_id):
    match = df[df["tree_id"].astype(str) == tree_id]
    if not match.empty:
        return match.iloc[0].to_frame().rename(columns={0: "value"})
    return None
