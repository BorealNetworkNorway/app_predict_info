# 🌲 Predict Project – Forest Plot  App

An quick application  to visualize the different forest plots as part of the **PREDICT project**.
---
https://predictprojectinfoapp.streamlit.app

### 🌍 Map of Norway (Folium)
* Displays all forest plots.

### 🧭 Plot Selection
* **Sidebar dropdown** to manually select a plot.

### 🌳 Tree Visualization
* Shows the **tree layout** in transformed polar coordinates.
* Trees are sized by **mean DBH**.
* Option to display **tree IDs**.

### 📐 Dendrometers
* Trees with **dendrometers** are listed right under the plot selector.
* A dedicated view highlights them. # I still need to work on it

---

## 💻 Project Infrastructure
```
predictmaps/
│
├── Home.py
├── utils.py
├── pages/
│   └── PlotDetails.xlsx
│   └── About.xlsx
├── data/
│   └── predict_tree_inventory_v3.xlsx
│   └── images/
├── requirements.txt
└── README.md
```
---

## ⚙️ Installation
#### Install dependencies

```bash
pip install -r requirements.txt
```
---
#### 📦 `requirements.txt`
These are the required libraries:
```txt
streamlit>=1.33.0
pandas>=2.0.0
numpy
folium
streamlit-folium
altair>=5.0#
```
( built with **Streamlit**, **Folium**, and **Altair**)

#### Run the Streamlit app

```bash
streamlit run app.py
```
---


## 📁  Customization | DATA 
* `data/predict_tree_inventory_v3.xlsx`: Contains all plot data.
Each sheet = one plot with the following columns :
plot_id |	location |	coordinates |	date |	tree_id |	species	| dbh1 |	dbh2 |	mean_dbh |	distance |	degrees |	cond |	can_position |	dendrometer_id |	dendrocircum |	comments |	health 2024 |	health 2025



## 🧪 To Do / Ideas
* Filter by species.
* Write what you want ☺ 

---

## 🧑‍💻 Authors
* \Aurorecgandd (Aurore Dallery) aka Lostinthewoods DJ
* The great Danielle Creek
* NMBU 
---

## 📜 License
...
