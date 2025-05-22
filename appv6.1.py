import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # For standard deviation calculation
from PIL import Image  # Import the Python Imaging Library (PIL) to handle images

# Set up the background image for the top section
def add_partial_background_image(image_url):
    partial_background_css = f"""
    <style>
    .top-section {{
        height: 25vh; /* Set height to 1/4 of the viewport */
        background: url("{image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    <div class="top-section"></div>
    """
    st.markdown(partial_background_css, unsafe_allow_html=True)

# Add your image URL here (can also be a local file served as a URL)
image_url = "https://globalprograms.unm.edu/assets/img/peng-logo-wide.png"  # Provided image URL
add_partial_background_image(image_url)

# Title directly under the image
st.markdown("""
    <h1 style='text-align: center;'>ENG-220 Group 7<br>Air Quality<br>Visualization Dashboard</h1>
""", unsafe_allow_html=True)

# Create a tab navigation bar
tab_selection = st.radio("Select Tab", ["Home", "About the Data"])

# Content for "Home" tab
if tab_selection == "Home":
    st.write("### Upload and Visualize Data")
    
    # File uploader for CSV
    data = pd.read_csv('./MaineDatav6.csv') 

    if data is not None:
        st.write("### Data Preview")
        st.dataframe(data)

        # Get total number of rows and columns
        total_rows, total_columns = data.shape

        # Inputs for start and end rows
        st.write("### Select Row Range for Analysis")
        start_row = st.number_input(
            "Start Row (0-indexed)", min_value=0, max_value=total_rows - 1, value=0, step=1
        )
        end_row = st.number_input(
            "End Row (0-indexed, inclusive)", min_value=start_row, max_value=total_rows - 1, value=total_rows - 1, step=1
        )

        # Filter the data for the selected row range
        filtered_data = data.iloc[start_row : end_row + 1]
        st.write("### Filtered Data Preview (Rows)")
        st.dataframe(filtered_data)

        # Multiselect for column filtering
        st.write("### Select Columns for Analysis")
        selected_columns = st.multiselect(
            "Select Columns",
            options=data.columns.tolist(),
            default=data.columns.tolist()  # Default to all columns
        )

        # Filter the data for selected columns
        filtered_data = filtered_data[selected_columns]
        st.write("### Filtered Data Preview (Rows & Columns)")
        st.dataframe(filtered_data)

        # Standard Deviation Calculator
        st.write("### Standard Deviation Calculator")
        std_column = st.selectbox("Select Column for Standard Deviation", selected_columns)
        if st.button("Calculate Standard Deviation"):
            try:
                std_values = filtered_data[std_column].astype(float)
                std_result = np.std(std_values, ddof=1)  # Using sample standard deviation
                st.success(f"The standard deviation of '{std_column}' is: {std_result}")
            except ValueError:
                st.error(f"Selected column '{std_column}' contains non-numeric data. Please select a numeric column.")

        # Average Calculator
        st.write("### Average Calculator")
        avg_column = st.selectbox("Select Column for Average", selected_columns)
        if st.button("Calculate Average"):
            try:
                avg_values = filtered_data[avg_column].astype(float)
                avg_result = np.mean(avg_values)  # Calculate the mean (average)
                st.success(f"The average of '{avg_column}' is: {avg_result}")
            except ValueError:
                st.error(f"Selected column '{avg_column}' contains non-numeric data. Please select a numeric column.")

        # Dropdown for selecting columns for plotting
        x_column = st.selectbox("Select X-axis column", selected_columns)
        y_column = st.selectbox("Select Y-axis column", selected_columns)

        # Dropdown for graph type
        graph_type = st.selectbox(
            "Select Graph Type",
            ["Line", "Scatter", "Bar", "Pie"]
        )

        # Plot button
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
                # Pie chart only makes sense for single-column data
                if len(filtered_data[x_column].unique()) <= 10:  # Limit to 10 unique categories for readability
                    plt.pie(
                        filtered_data[y_column],
                        labels=filtered_data[x_column],
                        autopct='%1.1f%%',
                        startangle=90,
                    )
                    plt.title(f"{y_column} (Pie Chart)")
                else:
                    st.error("Pie chart requires fewer unique categories in the X-axis.")

            if graph_type != "Pie":
                ax.set_xlabel(x_column)
                ax.set_ylabel(y_column)
                st.pyplot(fig)
            else:
                st.pyplot(plt)

        st.write("Tip: Ensure the selected columns are numeric for meaningful plots.")
    else:
        st.info("Please upload a CSV file to get started.")

# Content for "About the Data" tab
elif tab_selection == "About the Data":
    st.write("### About the Data")
    st.write(
        """
        This dataset contains air quality data collected from various monitoring stations.
        The data includes measurements of pollutants such as PM2.5, PM10, CO, and other 
        air quality indicators across different regions and times. 

        Two sets of data are included:
        1. **The raw data from 2020 to 2024**  
        The raw measurements collected for each year between 2020 and 2024.

        2. **The yearly average of the data from 2020 to 2024**  
        These are the average values calculated for each year, providing an overall view of the data trends over time.

        An average and standard deviation calculator is available to calculate more specific data, allowing users to perform more in-depth statistical analysis.
        """
    )

    # Reference the image stored in your GitHub repository (use raw URL)
    image_url = "https://raw.githubusercontent.com/OctuplePants/ENG220-Group-7/main/DATA.jpg"
    
    # Display the image
    st.image(image_url, caption="Air Quality Monitoring", use_column_width=True)

    # New section for detailed explanation about the data
    st.write(
        """
        ### Data Descriptions:
        
        **# Days with AQI**  
        Number of days in the year having an Air Quality Index value. This is the number of days on which measurements from any monitoring site in the county or MSA were reported to the AQS database.

        **# Days Good**  
        Number of days in the year having an AQI value 0 through 50.

        **# Days Moderate**  
        Number of days in the year having an AQI value 51 through 100.

        **# Days Unhealthy for Sensitive Groups**  
        Number of days in the year having an AQI value 101 through 150.

        **# Days Unhealthy**  
        Number of days in the year having an AQI value 151 through 200.

        **# Days Very Unhealthy**  
        Number of days in the year having an AQI value 201 through 300.

        **# Days Hazardous**  
        Number of days in the year having an AQI value 301 or higher.

        **AQI Max**  
        The highest daily AQI value in the year.

        **AQI 90th %ile**  
        90 percent of daily AQI values during the year were less than or equal to the 90th percentile value.

        **AQI Median**  
        Half of daily AQI values during the year were less than or equal to the median value, and half equaled or exceeded it.

        **# Days CO**  
        The number of days in the year when CO was the main pollutant.

        **# Days NO2**  
        The number of days in the year when NO2 was the main pollutant.

        **# Days O3**  
        The number of days in the year when O3 was the main pollutant.

        **# Days PM2.5**  
        The number of days in the year when PM2.5 was the main pollutant.

        **# Days PM10**  
        The number of days in the year when PM10 was the main pollutant.
        
        A daily index value is calculated for each air pollutant measured. The highest of those index values is the AQI value, and the pollutant responsible for...
        """
    )
