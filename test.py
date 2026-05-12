# # # import streamlit as st

# # # st.set_page_config(page_title="PatrolIQ | Dashboard", layout="wide")

# # # st.title("🛡️ PatrolIQ Command Center")
# # # st.markdown("""
# # # Welcome to the PatrolIQ management suite. Use the sidebar to navigate between 
# # # live tracking, historical analytics, and system configurations.
# # # """)

# # # # Example KPI Row
# # # col1, col2, col3 = st.columns(3)
# # # col1.metric("Active Patrols", "12", "2")
# # # col2.metric("Incidents Reported", "4", "-1")
# # # col3.metric("System Uptime", "99.9%")


# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import plotly.express as px
# # import folium
# # from streamlit_folium import st_folium
# # from folium.plugins import HeatMap
# # import mlflow


# # # If using a remote server (e.g., DagsHub, Databricks, or local server)
# # mlflow.set_tracking_uri("http://localhost:5000")

# # # --- 1. DATA CORE & SESSION STATE ---
# # def load_data():
# #     """Initializes the q2024 dataset with mock crime data."""
# #     dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="H")
# #     data = pd.DataFrame({
# #         "timestamp": dates,
# #         "lat": np.random.uniform(34.0, 34.1, len(dates)),
# #         "lon": np.random.uniform(-118.3, -118.2, len(dates)),
# #         "crime_type": np.random.choice([
# #             'HOMICIDE', 'CRIMINAL SEXUAL ASSAULT', 'ROBBERY', 'BATTERY', 
# #             'ASSAULT', 'BURGLARY', 'MOTOR VEHICLE THEFT', 'THEFT', 'VANDALISM'
# #         ], len(dates)),
# #         "severity": np.random.randint(1, 10, len(dates))
# #     })
# #     data["hour"] = data["timestamp"].dt.hour
# #     data["day"] = data["timestamp"].dt.day_name()
# #     return data

# # if "q2024" not in st.session_state:
# #     st.session_state.q2024 = load_data()

# # # --- 2. PAGE DEFINITIONS ---

# # def dashboard():
# #     st.title("🛡️ PatrolIQ Operations Dashboard")
# #     df = st.session_state.q2024
    
# #     col1, col2, col3 = st.columns(3)
# #     col1.metric("Total Incidents (2024)", len(df))
# #     col2.metric("High Severity Alerts", len(df[df["severity"] > 7]))
# #     col3.metric("Model Confidence", "94.2%")
    
# #     st.subheader("Incident Trends")
# #     chart_data = df.resample('M', on='timestamp').count()
# #     st.line_chart(chart_data["crime_type"])

# # def spatial_intel():
# #     st.title("📍 Spatial Intelligence & Clusters")
# #     df = st.session_state.q2024
    
# #     st.sidebar.subheader("Map Filters")
# #     crime_filter = st.sidebar.multiselect("Select Crime Types", df["crime_type"].unique(), default=df["crime_type"].unique())
# #     filtered_df = df[df["crime_type"].isin(crime_filter)]
    
# #     # Heatmap logic
# #     m = folium.Map(location=[34.05, -118.25], zoom_start=12, tiles="cartodbpositron")
# #     heat_data = [[row['lat'], row['lon']] for index, row in filtered_df.iterrows()]
# #     HeatMap(heat_data).add_to(m)
    
# #     # Placeholder for Cluster Boundaries (GeoJSON)
# #     st_folium(m, width=1000, height=500)
# #     st.caption("Heatmap showing density of reported incidents across metropolitan zones.")

# # def temporal_analysis():
# #     st.title("📈 Temporal Pattern Analysis")
# #     df = st.session_state.q2024
    
# #     # Heatmap Matrix: Day of Week vs Hour
# #     pivot = df.groupby(["day", "hour"]).size().reset_index(name="counts")
# #     fig = px.density_heatmap(pivot, x="hour", y="day", z="counts", 
# #                              color_continuous_scale="Viridis",
# #                              category_orders={"day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]})
# #     st.plotly_chart(fig, use_container_width=True)
# #     st.info("Concentrated darker areas indicate peak patrol demand periods.")

# # def ml_ops():
# #     st.title("🤖 Model Performance & MLflow")
    
# #     st.subheader("Dimensionality Reduction (U-MAP Projection)")
# #     # Simulating U-MAP 2D coordinates
# #     dr_data = pd.DataFrame(np.random.randn(100, 2), columns=['x', 'y'])
# #     dr_data['cluster'] = np.random.choice(['A', 'B', 'C'], 100)
    
# #     fig = px.scatter(dr_data, x='x', y='y', color='cluster', title="Latent Feature Space")
# #     st.plotly_chart(fig)
    
# #     st.divider()
# #     st.subheader("MLflow Experiment Tracking")
# #     st.code("Experiment ID: patrol_iq_v2\nRun Status: ACTIVE\nActive Model: PCA")
    
# #     # Mocking MLflow metrics
# #     metrics = {"Accuracy": 0.89, "Precision": 0.85, "Recall": 0.82}
# #     st.json(metrics)

# # # --- 3. NAVIGATION ROUTER ---

# # pg = st.navigation({
# #     "Overview": [st.Page(dashboard, title="Dashboard", icon="📊")],
# #     "Geospatial": [st.Page(spatial_intel, title="Crime Mapping", icon="🗺️")],
# #     "Analytics": [
# #         st.Page(temporal_analysis, title="Time Patterns", icon="⏰"),
# #         st.Page(ml_ops, title="Model Monitoring", icon="⚙️")
# #     ]
# # })

# # st.set_page_config(page_title="PatrolIQ", layout="wide")
# # pg.run()

# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import folium
# from streamlit_folium import st_folium
# from folium.plugins import HeatMap
# import mlflow

# # --- 1. DATA CORE & SESSION STATE ---

# @st.cache_data
# def load_data():
#     """Initializes the q2024 dataset with specific severity mapping."""
#     dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="H")
    
#     # Define specific severity mapping provided
#     severity_mapping = {
#         'HOMICIDE': 10,
#         'CRIMINAL SEXUAL ASSAULT': 9,
#         'OFFENSE INVOLVING CHILDREN': 8,
#         'ROBBERY': 7,
#         'BATTERY': 6,
#         'ASSAULT': 6,
#         'BURGLARY': 5,
#         'MOTOR VEHICLE THEFT': 5,
#         'CRIMINAL DAMAGE': 4,
#         'THEFT': 3,
#         'DECEPTIVE PRACTICE': 2,
#         'OTHER OFFENSE': 1
#     }

#     data = pd.DataFrame({
#         "timestamp": dates,
#         "lat": np.random.uniform(34.0, 34.1, len(dates)),
#         "lon": np.random.uniform(-118.3, -118.2, len(dates)),
#         "crime_type": np.random.choice(list(severity_mapping.keys()), len(dates))
#     })

#     # Apply the mapping (Mechanical necessity for Step 8 analysis)
#     data['Severity_Score'] = data['crime_type'].map(severity_mapping).fillna(1)
    
#     data["hour"] = data["timestamp"].dt.hour
#     data["day"] = data["timestamp"].dt.day_name()
#     return data

# if "q2024" not in st.session_state:
#     st.session_state.q2024 = load_data()

# # --- 2. PAGE DEFINITIONS ---

# def dashboard():
#     st.title("🛡️ PatrolIQ Operations Dashboard")
#     df = st.session_state.q2024
    
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Incidents (2024)", f"{len(df):,}")
#     # High severity defined as 7 or higher per project specs
#     col2.metric("High Severity Alerts", len(df[df["Severity_Score"] >= 7]))
#     col3.metric("Avg City Severity", round(df['Severity_Score'].mean(), 2))
    
#     st.subheader("Incident Trends")
#     chart_data = df.resample('M', on='timestamp').count()
#     st.line_chart(chart_data["crime_type"])

# def spatial_intel():
#     st.title("📍 Spatial Intelligence & Clusters")
#     df = st.session_state.q2024
    
#     st.sidebar.markdown("### Map Filters")
#     # Matching the specific multi-select look from your screenshot
#     crime_filter = st.sidebar.multiselect(
#         "Select Crime Types", 
#         options=sorted(df["crime_type"].unique()), 
#         default=["ASSAULT", "THEFT", "VANDALISM"] if "VANDALISM" in df["crime_type"].values else [df["crime_type"].unique()[0]]
#     )
    
#     filtered_df = df[df["crime_type"].isin(crime_filter)]
    
#     # Heatmap logic using weighted Severity_Score
#     m = folium.Map(location=[34.05, -118.25], zoom_start=12, tiles="cartodbpositron")
    
#     # Weighting the heatmap by Severity_Score makes the visualization more meaningful
#     heat_data = [[row['lat'], row['lon'], row['Severity_Score']] for index, row in filtered_df.iterrows()]
#     HeatMap(heat_data, radius=15, blur=18).add_to(m)
    
#     st_folium(m, width=1000, height=500)
#     st.caption("Visualizing geographical clusters weighted by incident severity.")

# def temporal_analysis():
#     st.title("📈 Temporal Pattern Analysis")
#     df = st.session_state.q2024
    
#     pivot = df.groupby(["day", "hour"]).size().reset_index(name="counts")
#     fig = px.density_heatmap(
#         pivot, x="hour", y="day", z="counts", 
#         color_continuous_scale="Viridis",
#         category_orders={"day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
#     )
#     st.plotly_chart(fig, use_container_width=True)
#     st.info("Peak density indicates optimal time-windows for patrol deployment.")

# def ml_ops():
#     st.title("🤖 Model Performance & MLflow")
    
#     st.subheader("Interactive Dimensionality Reduction (U-MAP)")
#     dr_data = pd.DataFrame(np.random.randn(100, 2), columns=['x', 'y'])
#     dr_data['Severity'] = np.random.choice(['High', 'Medium', 'Low'], 100)
    
#     fig = px.scatter(dr_data, x='x', y='y', color='Severity', title="Latent Feature Cluster Analysis")
#     st.plotly_chart(fig)
    
#     st.divider()
#     st.subheader("MLflow Monitoring")
#     st.code("Active Model: PCA_Ensemble_v4\nTracking URI: http://localhost:5000")
#     st.json({"Accuracy": 0.89, "Precision": 0.85, "Recall": 0.82})

# # --- 3. NAVIGATION ROUTER ---

# pg = st.navigation({
#     "Overview": [st.Page(dashboard, title="Dashboard", icon="📊")],
#     "Geospatial": [st.Page(spatial_intel, title="Crime Mapping", icon="🗺️")],
#     "Analytics": [
#         st.Page(temporal_analysis, title="Time Patterns", icon="⏰"),
#         st.Page(ml_ops, title="Model Monitoring", icon="⚙️")
#     ]
# })

# st.set_page_config(page_title="PatrolIQ", layout="wide")
# pg.run()

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import mlflow
from mlflow.tracking import MlflowClient

# --- 1. MLFLOW CONFIGURATION ---
mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

# --- 2. DATA ENGINE (Bridging from Jupyter) ---
@st.cache_data
def get_cleaned_data():
    """
    Simulates the cleaning and mapping logic from Mainpatrol.ipynb
    """
    # In production, you would load your CSV: pd.read_csv('cleaned_crime_data.csv')
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="H")
    df = pd.DataFrame({
        "timestamp": dates,
        "lat": np.random.uniform(41.7, 42.0, len(dates)),  # Chicago-like coordinates
        "lon": np.random.uniform(-87.7, -87.5, len(dates)),
        "Primary Type": np.random.choice([
            'HOMICIDE', 'ROBBERY', 'ASSAULT', 'THEFT', 'BATTERY', 'VANDALISM'
        ], len(dates))
    })

    # Your Severity Mapping from the Notebook
    severity_mapping = {
        'HOMICIDE': 10, 'CRIMINAL SEXUAL ASSAULT': 9, 'OFFENSE INVOLVING CHILDREN': 8,
        'ROBBERY': 7, 'BATTERY': 6, 'ASSAULT': 6, 'BURGLARY': 5,
        'MOTOR VEHICLE THEFT': 5, 'CRIMINAL DAMAGE': 4, 'THEFT': 3,
        'DECEPTIVE PRACTICE': 2, 'OTHER OFFENSE': 1
    }

    df['Severity_Score'] = df['Primary Type'].map(severity_mapping).fillna(1)
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()
    return df

# Initialize session state for your schedule data variable
if "q2024" not in st.session_state:
    st.session_state.q2024 = get_cleaned_data()

# --- 3. PAGE MODULES ---

def spatial_intel_page():
    st.title("📍 Spatial Intelligence & Clusters")
    df = st.session_state.q2024
    
    st.sidebar.markdown("### Map Filters")
    crime_types = sorted(df["Primary Type"].unique())
    selected_crimes = st.sidebar.multiselect("Select Crime Types", crime_types, default=["HOMICIDE", "ROBBERY"])

    filtered_df = df[df["Primary Type"].isin(selected_crimes)]

    # Map with Weighted Heatmap
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=11, tiles="cartodbpositron")
    
    # Passing Severity_Score as the weight (3rd parameter)
    heat_data = [[row['lat'], row['lon'], row['Severity_Score']] for _, row in filtered_df.iterrows()]
    HeatMap(heat_data, radius=15, blur=15).add_to(m)
    
    st_folium(m, width=1100, height=550)
    st.info(f"Showing {len(filtered_df)} incidents. Heat intensity weighted by Severity Score.")

def temporal_analysis_page():
    st.title("📈 Temporal Pattern Analysis")
    df = st.session_state.q2024
    
    # Heatmap Matrix: Day vs Hour
    pivot = df.groupby(["day", "hour"]).size().reset_index(name="Incident Count")
    fig = px.density_heatmap(
        pivot, x="hour", y="day", z="Incident Count",
        color_continuous_scale="Reds",
        category_orders={"day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
    )
    st.plotly_chart(fig, use_container_width=True)

def ml_ops_page():
    st.title("🤖 Model Performance & MLflow")
    
    # Log / Retrieve from MLflow
    st.subheader("Clustering Metrics")
    col1, col2 = st.columns(2)
    
    # Mocking MLflow run data for the UI
    with col1:
        st.metric("Optimal K (Elbow)", "5")
        st.metric("Silhouette Score", "0.42")
    with col2:
        st.metric("Explained Variance (PCA)", "88%")
        st.metric("Reconstruction Error", "0.05")

    # MLflow Table
    st.divider()
    st.markdown("### Experiment Registry")
    try:
        runs = mlflow.search_runs(experiment_names=["PatrolIQ_Crime_Analytics"])
        st.dataframe(runs[['run_id', 'params.k_clusters', 'metrics.silhouette', 'status']])
    except:
        st.warning("MLflow server not detected. Showing local registry simulation.")
        st.table({"Run ID": ["a1b2", "c3d4"], "Algorithm": ["K-Means", "DBSCAN"], "Status": ["Finished", "Failed"]})

# --- 4. NAVIGATION ROUTER ---

pg = st.navigation({
    "Operations": [st.Page(spatial_intel_page, title="Crime Mapping", icon="📍")],
    "Analytics": [
        st.Page(temporal_analysis_page, title="Time Patterns", icon="⏰"),
        st.Page(ml_ops_page, title="Model Monitoring", icon="⚙️")
    ]
})

st.set_page_config(page_title="PatrolIQ | Intelligence", layout="wide")
pg.run()