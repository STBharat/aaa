import streamlit as st
import os
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.card import card
from streamlit_extras.stylable_container import stylable_container

# Import components
from components.header import create_header
from components.upload import upload_section
from components.analysis import analysis_section
from components.timelapse import timelapse_section
from components.statistics import statistics_section
from components.time_series import time_series_analysis
from components.download import download_section
from components.action_fixed import action_section
from components.realtime_mapping import realtime_mapping_section
from components.global_map import global_forest_health_section

# Set page configuration
st.set_page_config(
    page_title="Deforestation Analysis Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS file
def load_css():
    with open('.streamlit/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply CSS styling
load_css()

# Initialize session state variables if they don't exist
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'analyzed_image' not in st.session_state:
    st.session_state.analyzed_image = None
if 'deforested_areas' not in st.session_state:
    st.session_state.deforested_areas = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = "Amazon Rainforest"
if 'prev_location' not in st.session_state:
    st.session_state.prev_location = None
# Initialize theme state
if 'theme' not in st.session_state:
    st.session_state.theme = "light"
if 'timelapse_images' not in st.session_state:
    st.session_state.timelapse_images = {}
if 'time_series_data' not in st.session_state:
    st.session_state.time_series_data = None
if 'forest_loss_stats' not in st.session_state:
    st.session_state.forest_loss_stats = {}

# Function to toggle theme
def toggle_theme():
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"
    # Force rerun to apply theme changes immediately
    st.rerun()  # Use the rerun method to refresh the app

# Apply current theme with dark mode class
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="stSidebar"], [data-testid="stMarkdown"] {
        color-scheme: dark;
    }
    
    /* Apply dark class to everything */
    body {
        class: dark;
    }
    
    .dark-mode-active {
        display: block;
    }
    
    /* Primary backgrounds */
    body, .main, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0e1117 !important;
        color: white !important;
    }
    
    /* Sidebar specific styling */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e !important;
        border-right: 1px solid #333333 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] [data-testid="stMarkdown"],
    [data-testid="stSidebar"] [role="radiogroup"] label span p {
        color: white !important;
    }
    
    /* Enhanced fix for sidebar selectbox */
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div:first-child,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div:first-child > div,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div:first-child > div > div,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] input {
        background-color: #2b2b2b !important;
        color: white !important;
    }
    
    /* Enhanced fix for selectbox option text */
    [data-testid="stSidebar"] ul[data-baseweb="menu"] li,
    [data-testid="stSidebar"] ul[data-baseweb="menu"] li div,
    [data-testid="stSidebar"] ul[data-baseweb="menu"] li div span,
    ul[data-baseweb="menu"] li div span {
        color: white !important;
    }
    
    ul[data-baseweb="menu"] {
        background-color: #1e1e1e !important;
    }
    
    /* Improve dropdown items */
    [data-testid="stSidebar"] [role="listbox"] div,
    [data-testid="stSidebar"] [role="listbox"] span {
        color: white !important;
    }
    
    /* Enhanced Dark Mode Sidebar Styling */
    /* Comprehensive fix for all sidebar text elements */
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] .stSelectbox * label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] ul {
        color: white !important;
    }
    
    /* Sidebar navigation elements - extra specific */
    [data-testid="stSidebar"] [role="radiogroup"] label div span p,
    [data-testid="stSidebar"] [data-baseweb="select"] div div div,
    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] div span span,
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] span,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* Fix sidebar selectbox dropdown elements */
    [data-testid="stSidebar"] ul[data-baseweb="menu"] li,
    [data-testid="stSidebar"] ul[data-baseweb="menu"] li div,
    [data-testid="stSidebar"] ul[data-baseweb="menu"] li div span {
        color: white !important;
    }
    
    /* Fix radio buttons in sidebar with stronger selector */
    [data-testid="stSidebar"] div[role="radiogroup"] label,
    [data-testid="stSidebar"] div[role="radiogroup"] label div,
    [data-testid="stSidebar"] div[role="radiogroup"] label div span,
    [data-testid="stSidebar"] div[role="radiogroup"] label div span p {
        color: white !important;
    }
    
    /* Fix sidebar button */
    [data-testid="stSidebar"] button {
        color: white !important;
        background-color: #4caf50 !important;
        border-color: #388e3c !important;
    }
    
    /* Navigation and radio buttons */
    [role="radiogroup"] label {
        color: white !important;
    }
    
    [role="radiogroup"] svg {
        color: white !important;
    }
    
    /* All text elements */
    h1, h2, h3, h4, h5, h6, p, span, label, .element-container,
    .stMarkdown, .stText, [data-testid="stWidgetLabel"] {
        color: white !important;
    }
    
    /* Form inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        color: white !important;
        background-color: #1f2229 !important;
        border-color: #4b4b4b !important;
    }
    
    /* Selectboxes and dropdowns */
    .stSelectbox > div > div > div,
    .stMultiselect > div > div > div {
        color: white !important;
        background-color: #1f2229 !important;
        border-color: #4b4b4b !important;
    }
    
    /* Tables and dataframes */
    .stTable, .dataframe, th, td {
        color: white !important;
        border-color: #4b4b4b !important;
    }
    
    .dataframe {
        background-color: #1f2229 !important;
    }
    
    .stDataFrame {
        background-color: #0e1117 !important;
    }
    
    .stDataFrame [data-testid="stTable"] {
        background-color: #1f2229 !important;
        color: white !important;
    }
    
    .stDataFrame [data-testid="stTable"] th {
        background-color: #262730 !important;
        color: white !important;
        border-bottom: 1px solid #4b4b4b !important;
    }
    
    /* Buttons and sliders */
    .stButton button {
        background-color: #4caf50 !important; 
        color: white !important;
        font-weight: 500 !important;
        text-shadow: 0px 0px 1px rgba(0,0,0,0.3) !important;
    }
    
    .stButton button:hover {
        background-color: #45a049 !important;
        border-color: #555 !important;
    }
    
    /* Ensure all button text is visible */
    button, .stButton > button, div[data-testid="stForm"] button {
        color: white !important;
        background-color: #4caf50 !important;
        font-weight: 500 !important;
        text-shadow: 0px 0px 1px rgba(0,0,0,0.3) !important;
    }
    
    /* Radio buttons */
    .stRadio label, .stRadio div, .stRadio p {
        color: white !important;
    }
    
    /* All sliders */
    .stSlider label, .stSlider p, .stSlider div {
        color: white !important;
    }
    
    /* Info boxes */
    [data-testid="stInfo"] {
        background-color: rgba(30, 30, 30, 0.7) !important;
        color: white !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader, .streamlit-expanderContent {
        background-color: #1e1e1e !important;
        color: white !important;
    }
    
    /* All card elements */
    [data-testid="stCard"], .element-container div div div div [data-testid="stHorizontalBlock"] div div {
        background-color: #1e1e1e !important;
        color: white !important;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    
    /* Feature cards specific */
    .feature-card, .feature-card * {
        color: white !important;
    }
    
    .feature-card-title {
        color: #4caf50 !important;
        font-weight: bold !important;
    }
    
    /* Small text and captions */
    small, .stCaption, caption {
        color: #cccccc !important;
    }
    
    /* Links */
    a:not([style]) {
        color: #4caf50 !important;
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        color: white !important;
    }
    
    .stFileUploader > div > div > span {
        color: #cccccc !important;
    }
    
    /* Fix for file uploader text */
    .stFileUploader p, .stFileUploader span, .stFileUploader label {
        color: white !important;
    }
    
    /* Make sure file uploader instructions are visible */
    .uploadedFileData p, .stFileUploader [data-testid="stFileUploadDropzone"] p,
    [data-testid="stFileUploadDropzone"] span, [data-testid="stFileUploadDropzone"] small {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add a class for CSS targeting
    st.markdown('<div class="dark-mode-active" style="display:none"></div>', unsafe_allow_html=True)
else:
    # Light theme - clean slate
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        color-scheme: light;
    }
    body {
        color: #262730;
        background-color: white;
    }
    .stApp {
        background-color: white;
    }
    .dark-mode-active {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Create a basic header by default - we'll show the dashboard elements only on the dashboard page

# Enhanced Sidebar with better organization
# Navigation section with icon - using header for cleaner look
st.sidebar.title("🧭 Navigation")

# Main sections with Dashboard as a separate option
main_sections = [
    "Dashboard",
    "Upload & Analysis",
    "Reports & Monitoring",
    "Take Action"
]

# Select the main section first
selected_main_section = st.sidebar.selectbox(
    "Main Sections",
    main_sections,
    index=0
)

# Define subsections for each main section
dashboard_options = [
    "Overview Dashboard",
    "Statistics & Metrics",
    "Time-Series Analysis",
    "Global Forest Health"
]

upload_analysis_options = [
    "Upload Satellite Image",
    "Analysis Results"
]

reports_monitoring_options = [
    "Real-Time Monitoring",
    "Time-lapse View",
    "Download Reports"
]

action_options = [
    "Take Action"
]

# Dictionary to get the appropriate options based on the selected main section
section_options = {
    "Dashboard": dashboard_options,
    "Upload & Analysis": upload_analysis_options,
    "Reports & Monitoring": reports_monitoring_options,
    "Take Action": action_options
}

# Icons for each subsection
all_options_with_icons = {
    "Overview Dashboard": "📊 Overview Dashboard",
    "Upload Satellite Image": "📤 Upload Satellite Image",
    "Analysis Results": "🔍 Analysis Results",
    "Time-lapse View": "⏱️ Time-lapse View",
    "Real-Time Monitoring": "🔴 Real-Time Monitoring",
    "Statistics & Metrics": "📈 Statistics & Metrics",
    "Time-Series Analysis": "📉 Time-Series Analysis",
    "Global Forest Health": "🌍 Global Forest Health",
    "Download Reports": "📁 Download Reports",
    "Take Action": "🌱 Take Action"
}

# Get options for the selected main section
current_options = section_options[selected_main_section]

# Convert options to their formatted versions with icons
formatted_options = [all_options_with_icons[option] for option in current_options]

# Create a dictionary to map formatted options back to original options
option_map = {formatted: original.split(" ")[-1] for original, formatted in all_options_with_icons.items()}

# Display radio buttons with formatted options for the subsection
selected_formatted = st.sidebar.radio(
    f"{selected_main_section} Options",
    formatted_options
)

# Map the selected formatted option back to the original option
subsection = option_map[selected_formatted]

# Define the actual page to display
if selected_main_section == "Dashboard":
    if subsection == "Dashboard":
        page = "Overview Dashboard"
    else:
        page = subsection
elif selected_main_section == "Upload & Analysis":
    if subsection == "Image":
        page = "Upload Satellite Image"
    else:
        page = "Analysis Results"
elif selected_main_section == "Reports & Monitoring":
    if subsection == "Monitoring":
        page = "Real-Time Monitoring"
    elif subsection == "View":
        page = "Time-lapse View"
    else:
        page = "Download Reports"
else:  # Take Action
    page = "Take Action"

st.sidebar.markdown("---")

# About section with clean styling
st.sidebar.header("🌍 About")
st.sidebar.markdown(
    """
    This dashboard visualizes deforestation using satellite imagery and advanced analytics. 
    
    🔍 Upload your own satellite imagery or explore our sample locations.
    
    📊 Analyze patterns, view statistics, and monitor changes over time.
    """
)

st.sidebar.markdown("---")

# Appearance section
st.sidebar.header("🎨 Appearance")
current_theme = "Dark" if st.session_state.theme == "dark" else "Light"
st.sidebar.markdown(f"**Current theme:** {current_theme}")
theme_toggle = st.sidebar.button(
    f"Switch to {'Light' if current_theme == 'Dark' else 'Dark'} Mode", 
    on_click=toggle_theme,
    key="theme_toggle",
    help="Switch between dark and light mode"
)

st.sidebar.markdown("---")

# Sample locations section with professional styling
st.sidebar.header("🗺️ Sample Locations")
location = st.sidebar.selectbox(
    "Select a region to analyze",
    ["Amazon Rainforest", "Borneo", "Congo Basin", "Custom Upload"]
)

# Style for location info items
location_info_style = "padding-left: 10px; margin: 5px 0; border-left: 2px solid #4caf50;"

# Add detailed information about the selected location
if location == "Amazon Rainforest":
    st.sidebar.markdown("**Amazon Rainforest**: The largest tropical rainforest in the world, spanning 9 countries.")
    st.sidebar.markdown(f"<div style='{location_info_style}'>🌧️ <b>Annual Rainfall</b>: 2,000-3,000 mm</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='{location_info_style}'>🌳 <b>Tree Species</b>: 16,000+</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='{location_info_style}'>🔥 <b>Deforestation Rate</b>: 0.9% annually</div>", unsafe_allow_html=True)
elif location == "Borneo":
    st.sidebar.markdown("**Borneo**: The third-largest island in the world with ancient rainforests.")
    st.sidebar.markdown(f"<div style='{location_info_style}'>🌧️ <b>Annual Rainfall</b>: 2,500-4,000 mm</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='{location_info_style}'>🦧 <b>Endemic Species</b>: 222 mammals</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='{location_info_style}'>🔥 <b>Deforestation Rate</b>: 1.3% annually</div>", unsafe_allow_html=True)
elif location == "Congo Basin":
    st.sidebar.markdown("**Congo Basin**: Africa's largest contiguous forest and the second-largest tropical rainforest globally.")
    st.sidebar.markdown(f"<div style='{location_info_style}'>🌧️ <b>Annual Rainfall</b>: 1,700-2,200 mm</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='{location_info_style}'>🌳 <b>Area</b>: 2 million square kilometers</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='{location_info_style}'>🔥 <b>Deforestation Rate</b>: 0.3% annually</div>", unsafe_allow_html=True)
elif location == "Custom Upload":
    st.sidebar.markdown("**Custom Upload**: Analyze your own satellite imagery.")
    st.sidebar.markdown(f"<div style='{location_info_style}'>📤 Upload satellite imagery in the Upload section</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='{location_info_style}'>⚙️ Our AI will process and analyze your data</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='{location_info_style}'>📊 View detailed deforestation metrics and visualization</div>", unsafe_allow_html=True)

# Add a small note about data sources
st.sidebar.markdown("---")
st.sidebar.markdown("<small>*Data reflects most recent available statistics. Sources include global forest monitoring agencies and satellite data aggregators.</small>", unsafe_allow_html=True)

if location != st.session_state.selected_location:
    # Store previous location before changing
    st.session_state.prev_location = st.session_state.selected_location
    # Update to new location
    st.session_state.selected_location = location
    st.session_state.analysis_complete = False
    if location != "Custom Upload":
        # This would load predetermined data for the selected location
        st.session_state.analysis_complete = True
    st.rerun()

# Main content based on selected page
if page == "Overview Dashboard":
    # Show full dashboard header with statistics and cards
    from components.header import create_header
    create_header(show_dashboard_elements=True)
    
    # Show brief stats in cards at the top
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="padding: 20px; border-radius: 10px; background-color: rgba(76, 175, 80, 0.1); border-left: 4px solid #4CAF50;">
            <h3 style="margin-top: 0;">Global Status</h3>
            <div style="font-size: 24px; font-weight: bold; color: #4CAF50;">12.2 million</div>
            <div>hectares of tropical forest lost in 2024</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 20px; border-radius: 10px; background-color: rgba(244, 67, 54, 0.1); border-left: 4px solid #F44336;">
            <h3 style="margin-top: 0;">Alert Status</h3>
            <div style="font-size: 24px; font-weight: bold; color: #F44336;">132</div>
            <div>active deforestation alerts this week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="padding: 20px; border-radius: 10px; background-color: rgba(33, 150, 243, 0.1); border-left: 4px solid #2196F3;">
            <h3 style="margin-top: 0;">Current Location</h3>
            <div style="font-size: 24px; font-weight: bold; color: #2196F3;">{}</div>
            <div>selected for monitoring</div>
        </div>
        """.format(st.session_state.selected_location), unsafe_allow_html=True)
    
    # Brief introduction section
    st.markdown("""
    ### Welcome to the Deforestation Analysis Dashboard
    This interactive platform provides comprehensive tools to monitor, analyze, and understand deforestation patterns 
    using satellite imagery and advanced analytics. Select different sections from the navigation menu to explore 
    specific features and analysis tools.
    """)
    
    # Display key visualizations
    dashboard_tabs = st.tabs(["Map View", "Recent Statistics", "Quick Upload"])
    
    with dashboard_tabs[0]:
        st.subheader("Interactive Map View")
        st.info("Interactive map showing deforestation hotspots in the selected region.")
        
        # Import and use functions from other components for the map view
        from data.sample_coordinates import get_coordinates_for_location
        from utils.mapping import create_map_with_deforestation
        
        coordinates = get_coordinates_for_location(st.session_state.selected_location)
        map_view = create_map_with_deforestation(
            center_lat=coordinates["lat"],
            center_lon=coordinates["lon"],
            zoom=coordinates["zoom"],
            deforested_areas=st.session_state.deforested_areas if 'deforested_areas' in st.session_state else None
        )
        
        from streamlit_folium import folium_static
        folium_static(map_view)
        
    with dashboard_tabs[1]:
        st.subheader("Recent Deforestation Statistics")
        
        # Sample statistic visualization
        from utils.visualization import create_comparison_chart
        
        # Create a sample comparison chart
        locations = ["Amazon Rainforest", "Borneo", "Congo Basin"]
        comparison_chart = create_comparison_chart(locations)
        st.plotly_chart(comparison_chart, use_container_width=True)
        
        # Show a brief metrics table
        import pandas as pd
        metrics_data = {
            "Region": ["Amazon", "Borneo", "Congo Basin", "Global"],
            "Forest Loss (hectares)": ["1.5M", "940K", "790K", "12.2M"],
            "% Change (YoY)": ["-2.3%", "+1.7%", "-0.5%", "-0.8%"],
            "Primary Cause": ["Agriculture", "Palm Oil", "Logging", "Mixed"]
        }
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True)
        
    with dashboard_tabs[2]:
        st.subheader("Quick Satellite Image Upload")
        st.write("Upload a satellite image for quick analysis, or navigate to the full Upload & Analysis section for detailed comparison.")
        
        quick_upload = st.file_uploader(
            "Choose a satellite image for quick analysis",
            type=["jpg", "jpeg", "png"],
            key="dashboard_uploader"
        )
        
        if quick_upload is not None:
            from PIL import Image
            
            try:
                # Read and display the uploaded image
                image = Image.open(quick_upload)
                st.image(image, caption="Uploaded Image", use_container_width=True)
                
                # Add a button to redirect to the full analysis page
                if st.button("Proceed to Full Analysis"):
                    st.session_state.uploaded_image = image
                    # We'll use the session state to track that we want to switch to the upload section
                    st.session_state.redirect_to_upload = True
                    st.rerun()
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
    
    # Check if we need to redirect to the upload section
    if 'redirect_to_upload' in st.session_state and st.session_state.redirect_to_upload:
        # Clear the redirect flag
        st.session_state.redirect_to_upload = False
        # This would normally redirect to the upload section

elif page == "Upload Satellite Image":
    # Show basic header for non-dashboard pages
    from components.header import create_header
    create_header(show_dashboard_elements=False)
    upload_section()
    
elif page == "Analysis Results":
    from components.header import create_header
    create_header(show_dashboard_elements=False)
    analysis_section()
    
elif page == "Time-lapse View":
    from components.header import create_header
    create_header(show_dashboard_elements=False)
    timelapse_section()
    
elif page == "Real-Time Monitoring":
    from components.header import create_header
    create_header(show_dashboard_elements=False)
    realtime_mapping_section()
    
elif page == "Statistics & Metrics":
    from components.header import create_header
    create_header(show_dashboard_elements=False)
    
    # Ensure statistics section is called with proper error handling
    try:
        # Force analysis complete to be true for statistics to display
        if 'analysis_complete' not in st.session_state:
            st.session_state.analysis_complete = True
        if not st.session_state.analysis_complete:
            st.session_state.analysis_complete = True
            
        # Call the statistics section
        statistics_section()
    except Exception as e:
        st.error(f"Error displaying statistics: {str(e)}")
        st.write("Reloading statistics component...")
        statistics_section()
    
elif page == "Time-Series Analysis":
    from components.header import create_header
    create_header(show_dashboard_elements=False)
    time_series_analysis()
    
elif page == "Global Forest Health":
    from components.header import create_header
    create_header(show_dashboard_elements=False)
    global_forest_health_section()
    
elif page == "Download Reports":
    from components.header import create_header
    create_header(show_dashboard_elements=False)
    download_section()
    
elif page == "Take Action":
    from components.header import create_header
    create_header(show_dashboard_elements=False)
    action_section()

# Footer
st.markdown("---")
st.markdown("© 2025 Deforestation Analysis Dashboard | Built with Streamlit")
