import streamlit as st
import pandas as pd
import plotly.express as px
from api import apod_generator

st.set_page_config(page_title="Water Quality Dashboard",
    layout="wide")

# ---------- OVERVIEW ----------
st.title("Water Quality Dashboard")
st.header("Interactive Data Visualization for Water Quality Monitoring")
st.caption("Course: Internship Ready Software Development – Prof. Gregory Reis - Anxhela Nano")

st.markdown(
    """
    This app lets you explore **water quality** data from Biscayne Bay.\n
    Use the controls in the sidebar to upload your own CSV or filter the default dataset.
    """
)

st.divider()

# ---------- SIDEBAR: USER INPUT ----------
st.sidebar.title("Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload a water quality CSV",
    type=["csv"],
    help="If no file is uploaded, the default Biscayne Bay dataset is used."
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Custom dataset loaded.")
else:
    df = pd.read_csv("biscayneBay_waterquality.csv")
    st.sidebar.info("Using default Biscayne Bay dataset.")

# Example interactive filters (adjust column names to match your CSV)
# Filter by temperature range
if "Temperature (c)" in df.columns:
    min_temp = float(df["Temperature (c)"].min())
    max_temp = float(df["Temperature (c)"].max())
    temp_range = st.sidebar.slider(
        "Filter by temperature (°C)",
        min_value=min_temp,
        max_value=max_temp,
        value=(min_temp, max_temp)
    )
    df = df[(df["Temperature (c)"] >= temp_range[0]) &
            (df["Temperature (c)"] <= temp_range[1])]

# Optional pH filter if pH column exists
if "pH" in df.columns:
    ph_min = float(df["pH"].min())
    ph_max = float(df["pH"].max())
    ph_range = st.sidebar.slider(
        "Filter by pH",
        min_value=ph_min,
        max_value=ph_max,
        value=(ph_min, ph_max)
    )
    df = df[(df["pH"] >= ph_range[0]) & (df["pH"] <= ph_range[1])]

st.sidebar.markdown("---")
show_descriptive = st.sidebar.checkbox("Show descriptive statistics", value=True)

# ---------- MAIN TABS ----------
tab_overview, tab_2d, tab_3d, tab_apod = st.tabs(
    ["Overview & Data", "2D Visualizations", "3D Visualizations", "NASA APOD"]
)

# ----- TAB 1: Overview & Data -----
with tab_overview:
    st.subheader("Dataset Overview")
    st.markdown(
        """
        This section shows the raw water quality data and basic descriptive statistics.\n
        Use it to understand ranges, missing values, and general trends in the dataset.
        """
    )

    st.write("### Raw Data")
    st.dataframe(df)

    if show_descriptive:
        st.write("### Descriptive Statistics")
        st.dataframe(df.describe())

# ----- TAB 2: 2D PLOTS -----
with tab_2d:
    st.subheader("2D Visualizations")
    st.markdown(
        """
        The plots below help you explore **relationships** between water quality variables.\n
        Use them to identify correlations and patterns (e.g., how temperature relates to oxygen levels).
        """
    )

    # Let user select x and y axes from numeric columns
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)

        with col1:
            x_col = st.selectbox("X-axis variable", numeric_cols, index=0)
        with col2:
            y_col = st.selectbox("Y-axis variable", numeric_cols, index=min(1, len(numeric_cols) - 1))

        color_col = None
        if "pH" in df.columns:
            color_col = "pH"

        fig_scatter = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=f"Scatter Plot: {y_col} vs {x_col}",
            labels={x_col: x_col, y_col: y_col},
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Time series if a time column exists
    if "Time" in df.columns and "Temperature (c)" in df.columns:
        st.markdown("### Temperature Over Time")
        fig_line = px.line(
            df,
            x="Time",
            y="Temperature (c)",
            title="Water Temperature Over Time",
            labels={"Time": "Time", "Temperature (c)": "Temperature (°C)"}
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ----- TAB 3: 3D PLOTS -----
with tab_3d:
    st.subheader("3D Visualization of the Water Column")
    st.markdown(
        """
        This 3D scatter plot shows sampling locations and depth.\n
        The **color** encodes temperature, and the **z-axis** represents water column depth.
        """
    )

    required_3d_cols = {"Longitude", "Latitude", "Total Water Column (m)"}
    if required_3d_cols.issubset(set(df.columns)) and "Temperature (c)" in df.columns:
        fig_3d = px.scatter_3d(
            df,
            x="Longitude",
            y="Latitude",
            z="Total Water Column (m)",
            color="Temperature (c)",
            title="3D View of Water Column and Temperature",
            labels={
                "Longitude": "Longitude",
                "Latitude": "Latitude",
                "Total Water Column (m)": "Total Depth (m)",
                "Temperature (c)": "Temperature (°C)",
            }
        )
        fig_3d.update_scenes(zaxis_autorange="reversed")
        st.plotly_chart(fig_3d, use_container_width=True)
    else:
        st.warning(
            "3D plot requires 'Longitude', 'Latitude', 'Total Water Column (m)', and 'Temperature (c)' columns."
        )

# ----- TAB 4: NASA APOD -----
with tab_apod:
    st.subheader("NASA Astronomy Picture of the Day")
    st.markdown(
        """
        This section demonstrates using an **external API** (NASA APOD) inside the app.\n
        Make sure you have a valid `NASA_API_KEY` set in your environment or on Streamlit Cloud.
        """
    )

    if st.button("Load today's APOD"):
        try:
            apod_data = apod_generator()
            st.image(apod_data.get("url"), caption=apod_data.get("title"))
            st.write(apod_data.get("explanation"))
        except Exception as e:
            st.error(f"Error loading APOD: {e}")
