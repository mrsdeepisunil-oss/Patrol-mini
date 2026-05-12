import streamlit as st
import pandas as pd
import numpy as np
import mlflow.sklearn
import folium
from streamlit_folium import st_folium
import joblib
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="PatrolIQ: Chicago Safety Dashboard", layout="wide")

# --- LOAD MODELS FROM MLFLOW ---
@st.cache_resource # Keeps the models in memory so they don't reload every click
def load_production_assets():
    # Load Geographic Model
    model = mlflow.sklearn.load_model("models:/Patrol_Clustering_Prod/Production")
    
    # Load Artifacts (Assuming you logged them to the same run)
    # For now, if you have them locally, we use joblib
    scaler = joblib.load("scaler.pkl")
    pca = joblib.load("pca_transformer.pkl")
    
    return model, scaler, pca

try:
    model, scaler, pca = load_production_assets()
    st.sidebar.success("✅ Production Models Loaded")
except Exception as e:
    st.sidebar.error(f"❌ Error loading models: {e}")

# --- DASHBOARD UI ---
st.title("🏙️ PatrolIQ: Smart Safety Analytics")
st.markdown("### Chicago Police Department Resource Allocation Tool")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Patrol Simulation")
lat = st.sidebar.number_input("Latitude", value=41.8781, format="%.4f")
lon = st.sidebar.number_input("Longitude", value=-87.6298, format="%.4f")

if st.sidebar.button("Identify Patrol Zone"):
    # 1. Prepare input
    input_data = pd.DataFrame([[lat, lon]], columns=['Latitude', 'Longitude'])
    
    # 2. Add dummy columns if your scaler expects more features (hour, etc.)
    # Note: Ensure this matches your training feature count!
    
    # 3. Predict
    # (Example logic: Scale -> PCA -> Predict)
    # prediction = model.predict(pca_input)
    
    st.sidebar.write(f"Targeting: **Zone {np.random.randint(0,10)}**") # Placeholder logic

# --- INTERACTIVE MAP ---
st.subheader("High-Density Crime Hotspots")
m = folium.Map(location=[41.8781, -87.6298], zoom_start=11, tiles="CartoDB positron")

# Example: Plotting a few hotspots from your clusters
# In your final version, you'll loop through df_cleaned here
folium.CircleMarker(
    location=[41.8781, -87.6298],
    radius=10,
    color="red",
    fill=True,
    popup="High Risk Zone"
).add_to(m)

st_folium(m, width=1200, height=600)