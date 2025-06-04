# -*- coding: utf-8 -*-
# Group 007 - Maine Air Quality Dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Title
st.title("Group-007")

st.markdown("""
### Air Quality Visualization Dashboard for Maine

This project, developed for a Peace Engineering course, provides an interactive dashboard to visualize and analyze air quality data in **Maine**.  
The dashboard uses **Python and Streamlit** to enable statistical analysis and graphical exploration of trends in air quality.

#### Key Features:
- 📊 **Data Preview**: Filter rows and columns interactively
- 📈 **Visualizations**: Line, scatter, bar, and pie charts
- 📐 **Stats Tools**: Compute standard deviation and average on selected fields
- 🗂️ **Dataset Scope**: Data from **2020 to 2024**, including:
    - Days categorized by AQI levels (Good, Moderate, Unhealthy, etc.)
    - Specific pollutants (CO, NO₂, O₃, PM2.5, PM10)
    - AQI summaries (Max, Median, 90th Percentile)

---
""")

# Load CSV from local path
try:
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "MaineDatav6.csv")
    data = pd.read_csv(csv_path)

    st.subheader("Data Preview")
    st.dataframe(data)

    # Row filter
    total_rows, total_columns = data.shape
    start_row = st.number_input("Start Row", 0, total_rows - 1, 0)
    end_row = st.number_input("End Row", start_row, total_rows - 1, total_rows - 1)
    filtered_data = data.iloc[start_row:end_row + 1]

    st.subheader("Filtered Data (Rows)")
    st.dataframe(filtered_data)

    # Column filter
    selected_columns = st.multiselect("Select Columns", options=data.columns.tolist(), default=data.columns.tolist())
    filtered_data = filtered_data[selected_columns]

    st.subheader("Filtered Data (Rows & Columns)")
    st.dataframe(filtered_data)

    # Standard deviation
    st.subheader("Standard Deviation Calculator")
    std_column = st.selectbox("Select Column for Standard Deviation", selected_columns)
    if st.button("Calculate Standard Deviation"):
        try:
            std_values = filtered_data[std_column].astype(float)
            std_result = np.std(std_values, ddof=1)
            st.success(f"The standard deviation of '{std_column}' is: {std_result}")
        except ValueError:
            st.error(f"Selected column '{std_column}' contains non-numeric data.")

    # Average
    st.subheader("Average Calculator")
    avg_column = st.selectbox("Select Column for Average", selected_columns)
    if st.button("Calculate Average"):
        try:
            avg_values = filtered_data[avg_column].astype(float)
            avg_result = np.mean(avg_values)
            st.success(f"The average of '{avg_column}' is: {avg_result}")
        except ValueError:
            st.error(f"Selected column '{avg_column}' contains non-numeric data.")

    # Graph plotting
    st.subheader("Graphical Visualization")
    x_column = st.selectbox("Select X-axis column", selected_columns)
    y_column = st.selectbox("Select Y-axis column", selected_columns)
    graph_type = st.selectbox("Select Graph Type", ["Line", "Scatter", "Bar", "Pie"])

    if st.button("Plot Graph"):
        fig, ax = plt.subplots()

        if graph_type == "Line":
            ax.plot(filtered_data[x_column], filtered_data[y_column], marker='o')
            ax.set_title(f"{y_column} vs {x_column} (Line Plot)")

        elif graph_type == "Scatter":
            ax.scatter(filtered_data[x_column], filtered_data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")

        elif graph_type == "Bar":
            ax.bar(filtered_data[x_column], filtered_data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")

        elif graph_type == "Pie":
            if len(filtered_data[x_column].unique()) <= 10:
                plt.pie(
                    filtered_data[y_column],
                    labels=filtered_data[x_column],
                    autopct='%1.1f%%',
                    startangle=90,
                )
                plt.title(f"{y_column} (Pie Chart)")
            else:
                st.error("Pie chart requires fewer than 10 unique categories.")

        if graph_type != "Pie":
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)
        else:
            st.pyplot(plt)

    st.info("Tip: Select numeric fields for meaningful statistics and plots.")

except FileNotFoundError:
    st.error("The file 'MaineDatav6.csv' was not found. Please make sure it is in the same folder as this script.")
