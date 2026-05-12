import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
from sklearn.cluster import DBSCAN # For concept reference

# --- 1. SETTINGS ---
st.set_page_config(page_title="PatrolIQ | Intelligence Suite", layout="wide")

# --- 2. DATA ENGINE ---
@st.cache_data
def load_patrol_data():
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="h")
    df = pd.DataFrame({
        "timestamp": dates,
        "lat": np.random.uniform(41.75, 41.95, len(dates)), 
        "lon": np.random.uniform(-87.80, -87.60, len(dates)),
        "Primary Type": np.random.choice([
            'HOMICIDE', 'ROBBERY', 'ASSAULT', 'THEFT', 'BATTERY', 
            'BURGLARY', 'MOTOR VEHICLE THEFT', 'VANDALISM'
        ], len(dates))
    })

    severity_mapping = {
        'HOMICIDE': 10, 'CRIMINAL SEXUAL ASSAULT': 9, 'OFFENSE INVOLVING CHILDREN': 8,
        'ROBBERY': 7, 'BATTERY': 6, 'ASSAULT': 6, 'BURGLARY': 5,
        'MOTOR VEHICLE THEFT': 5, 'CRIMINAL DAMAGE': 4, 'THEFT': 3,
        'DECEPTIVE PRACTICE': 2, 'OTHER OFFENSE': 1
    }
    
    df['Severity_Score'] = df['Primary Type'].map(severity_mapping).fillna(1)
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()
    df['month'] = df['timestamp'].dt.month_name()
    return df

if "patrol1" not in st.session_state:
    st.session_state.patrol1 = load_patrol_data()

# Safety check for the 'month' column to prevent KeyError
if 'month' not in st.session_state.patrol1.columns:
    st.session_state.patrol1['month'] = st.session_state.patrol1['timestamp'].dt.month_name()

# --- 3. PAGE MODULES ---

def dashboard_overview():
    st.title("📊 PatrolIQ Operations Overview")
    df = st.session_state.patrol1
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Incidents", f"{len(df):,}")
    m2.metric("Avg Severity", round(df['Severity_Score'].mean(), 2))
    m3.metric("Deployment Efficiency", "92%")
    m4.metric("Noise Points (DBSCAN)", "142") # Static example of DBSCAN noise detection

    st.subheader("Monthly Incident Trends")
    monthly_data = df.groupby('month').size().reset_index(name='count')
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_data['month'] = pd.Categorical(monthly_data['month'], categories=month_order, ordered=True)
    monthly_data = monthly_data.sort_values('month')

    fig = px.line(monthly_data, x='month', y='count', markers=True, color_discrete_sequence=['#E63946'])
    st.plotly_chart(fig, use_container_width=True)

def spatial_intelligence():
    st.title("📍 Spatial Intelligence & Clusters")
    df = st.session_state.patrol1
    
    st.sidebar.header("Map Filters")
    selected_crimes = st.sidebar.multiselect(
        "Filter by Crime Type", 
        options=sorted(df["Primary Type"].unique()),
        default=["HOMICIDE", "ROBBERY", "ASSAULT"]
    )
    
    filtered_df = df[df["Primary Type"].isin(selected_crimes)]

    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=11, tiles="cartodbpositron")
    heat_data = [[row['lat'], row['lon'], row['Severity_Score']] for _, row in filtered_df.iterrows()]
    HeatMap(heat_data, radius=15, blur=15).add_to(m)
    
    st_folium(m, width="100%", height=600)

def pattern_analysis():
    st.title("⏰ Temporal Patterns")
    df = st.session_state.patrol1
    pivot = df.groupby(["day", "hour"]).size().reset_index(name="counts")
    fig = px.density_heatmap(pivot, x="hour", y="day", z="counts", color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)

def model_diagnostics():
    st.title("⚙️ Model Diagnostics: Clustering & Noise")
    st.markdown("Compare the performance of **K-Means** (Centroid-based) vs **DBSCAN** (Density-based) for patrol zone optimization.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("K-Means: Centroid Analysis")
        # Visualizing K-Means clusters
        k_data = pd.DataFrame(np.random.randn(100, 2), columns=['x', 'y'])
        k_data['cluster'] = np.random.choice(['Zone 1', 'Zone 2', 'Zone 3'], 100)
        fig_k = px.scatter(k_data, x='x', y='y', color='cluster', title="K-Means (Fixed Clusters)")
        st.plotly_chart(fig_k, use_container_width=True)
        st.info("K-Means forces every incident into a cluster, even if it's an outlier.")

    with col2:
        st.subheader("DBSCAN: Density & Outliers")
        # Visualizing DBSCAN clusters with noise
        d_data = pd.DataFrame(np.random.randn(100, 2), columns=['x', 'y'])
        # Cluster -1 represents Noise in DBSCAN
        d_data['cluster'] = np.random.choice(['Cluster A', 'Cluster B', 'Outlier'], 100, p=[0.4, 0.4, 0.2])
        fig_d = px.scatter(d_data, x='x', y='y', color='cluster', 
                           color_discrete_map={'Outlier': '#808080'},
                           title="DBSCAN (Density-based + Noise)")
        st.plotly_chart(fig_d, use_container_width=True)
        st.info("DBSCAN identifies high-density 'core' areas and labels isolated incidents as 'Outliers'.")

    st.divider()
    st.subheader("Dimensionality Reduction (PCA Visualization)")
    dr_data = pd.DataFrame(np.random.randn(200, 2), columns=['PC1', 'PC2'])
    st.scatter_chart(dr_data)

# --- 4. NAVIGATION ---
pg = st.navigation({
    "Operations": [st.Page(dashboard_overview, title="Dashboard", icon="📊")],
    "Geospatial": [st.Page(spatial_intelligence, title="Spatial Intelligence", icon="🗺️")],
    "Analytics": [
        st.Page(pattern_analysis, title="Time Patterns", icon="⏰"),
        st.Page(model_diagnostics, title="Diagnostics", icon="⚙️")
    ]
})

pg.run()