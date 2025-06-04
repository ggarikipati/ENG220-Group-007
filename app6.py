# -*- coding: utf-8 -*-
# Group 007 - Maine Air Quality Dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Optional: Add a small image header (optional styling)
def add_top_banner(image_url):
    css = f"""
    <style>
    .top-banner {{
        height: 20vh;
        background: url("{image_url}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    <div class="top-banner"></div>
    """
    st.markdown(css, unsafe_allow_html=True)

# Banner (optional)
image_url = "https://globalprograms.unm.edu/assets/img/peng-logo-wide.png"
add_top_banner(image_url)

# App Title and Description
st.markdown("<h1 style='text-align: center;'>Group-007: Maine Air Quality Dashboard</h1>", unsafe_allow_html=True)

st.markdown("""
### Overview

This interactive dashboard was developed for a Peace Engineering course to explore and analyze **air quality data in Maine** from **2020 to 2024**.  
Built with **Streamlit**, the app allows for filtering, statistical analysis, and visualization of pollutant and AQI data.

**Main Features**:
- View and filter raw air quality data.
- Calculate averages and standard deviations.
- Visualize pollutants and AQI trends via multiple chart types.
""")

# Tabs: Home | About the Data
tab_selection = st.radio("Select Tab", ["Home", "About the Data"])

# === HOME TAB ===
if tab_selection == "Home":
    st.write("### Data Upload and Exploration")

    try:
        # Load local CSV
        data = pd.read_csv(os.path.join(os.path.dirname(__file__), "MaineDatav6.csv"))
        st.dataframe(data)

        # Select range
        total_rows = data.shape[0]
        start_row = st.number_input("Start Row", 0, total_rows - 1, 0)
        end_row = st.number_input("End Row", start_row, total_rows - 1, total_rows - 1)
        filtered_data = data.iloc[start_row:end_row + 1]

        # Column filter
        selected_columns = st.multiselect("Select Columns", data.columns.tolist(), default=data.columns.tolist())
        filtered_data = filtered_data[selected_columns]
        st.dataframe(filtered_data)

        # Standard Deviation
        st.write("### Standard Deviation")
        std_col = st.selectbox("Select Column for Std Dev", selected_columns)
        if st.button("Calculate Standard Deviation"):
            try:
                std_result = np.std(filtered_data[std_col].astype(float), ddof=1)
                st.success(f"Standard Deviation of '{std_col}': {std_result}")
            except:
                st.error("Selected column must be numeric.")

        # Average
        st.write("### Average")
        avg_col = st.selectbox("Select Column for Average", selected_columns)
        if st.button("Calculate Average"):
            try:
                avg_result = np.mean(filtered_data[avg_col].astype(float))
                st.success(f"Average of '{avg_col}': {avg_result}")
            except:
                st.error("Selected column must be numeric.")

        # Visualization
        st.write("### Plot")
        x_col = st.selectbox("X-axis", selected_columns)
        y_col = st.selectbox("Y-axis", selected_columns)
        chart_type = st.selectbox("Chart Type", ["Line", "Scatter", "Bar", "Pie"])

        if st.button("Plot Graph"):
            fig, ax = plt.subplots()
            if chart_type == "Line":
                ax.plot(filtered_data[x_col], filtered_data[y_col], marker='o')
            elif chart_type == "Scatter":
                ax.scatter(filtered_data[x_col], filtered_data[y_col])
            elif chart_type == "Bar":
                ax.bar(filtered_data[x_col], filtered_data[y_col])
            elif chart_type == "Pie":
                if len(filtered_data[x_col].unique()) <= 10:
                    plt.pie(
                        filtered_data[y_col],
                        labels=filtered_data[x_col],
                        autopct='%1.1f%%',
                        startangle=90,
                    )
                else:
                    st.error("Pie chart requires fewer than 10 unique categories.")
                    st.stop()

            if chart_type != "Pie":
                ax.set_title(f"{y_col} vs {x_col}")
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                st.pyplot(fig)
            else:
                st.pyplot(plt)

        st.info("Tip: Select numeric columns for accurate statistical analysis and plots.")

    except FileNotFoundError:
        st.error("CSV file 'MaineDatav6.csv' not found. Please ensure it's in the same directory.")

# === ABOUT TAB ===
else:
    st.subheader("About the Dataset")
    st.markdown("""
    The dataset contains **air quality data for Maine** from **2020 to 2024**, including:
    - Number of days categorized by AQI levels (Good, Moderate, Unhealthy, etc.)
    - Specific pollutant readings (CO, NO2, O3, PM2.5, PM10)
    - AQI statistics: Max, Median, 90th Percentile

    It provides both **daily raw data** and **annual averages** for exploring air quality trends over time.
    """)

    # Display image from GitHub (optional)
    image_url = "https://raw.githubusercontent.com/OctuplePants/ENG220-Group-7/main/DATA.jpg"
    st.image(image_url, caption="Air Quality Monitoring", use_column_width=True)
