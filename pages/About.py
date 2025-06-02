import streamlit as st

st.set_page_config(page_title="About", layout="wide")

st.markdown("<h1 style='text-align:center;'>About the Forest Explorer</h1>", unsafe_allow_html=True)

st.markdown("""
## About the Application

This application allows users to explore forest plots as part of the **PREDICT project**. 
You can view plot-specific metadata, tree inventory, and visualize their geographical distribution.
Please contact aurore.dallery@insa-lyon.fr for any modifications/errors/bread_to_offer. 
---

### About the PREDICT Project
**PREDICT** is a scientific project led by the Norwegian University of Life Sciences (NMBU).  
It aims to study the impact of drought and increased temperatures on boreal forest ecosystems in Norway
Learn more about the project [here](https://www.nmbu.no/en/research/projects/predict).

---

### Data Sources
- **Geological data**: Provided by [geo.ngu.no](https://geo.ngu.no)
- **Mean temperature data**: Collected from [climatecharts.net](https://climatecharts.net)

---
""")
