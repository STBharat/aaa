import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
import numpy as np
from streamlit_folium import folium_static, st_folium
import json

# Function to load forest health indicators
def load_forest_health_data():
    """
    Load global forest health data.
    In a production environment, this would connect to a real database or API.
    
    Returns:
    --------
    pd.DataFrame: Dataframe with forest health indicators for different regions
    """
    # Generate a sample dataframe with forest health indicators for different regions
    regions = [
        "Amazon Rainforest", "Borneo", "Congo Basin", "Taiga Forest",
        "Southeast Asian Rainforest", "Daintree Rainforest", "Atlantic Forest",
        "Valdivian Forest", "New Guinea Rainforest", "Sundarbans",
        "Madagascar Rainforest", "Tongass National Forest", "Western Ghats",
        "Central American Forests", "Eastern Australian Forests"
    ]
    
    # Sample coordinates for these regions (these are approximate)
    coordinates = [
        [-3.4653, -62.2159],  # Amazon
        [0.8456, 114.3424],   # Borneo
        [-0.2295, 15.8271],   # Congo
        [64.2823, 100.2512],  # Taiga
        [14.7922, 101.9625],  # Southeast Asian
        [-16.1698, 145.4244], # Daintree
        [-22.3813, -42.9886], # Atlantic
        [-40.3467, -72.5913], # Valdivian
        [-5.6866, 142.8350],  # New Guinea
        [21.9497, 89.1833],   # Sundarbans
        [-18.7669, 46.8691],  # Madagascar
        [57.5905, -133.6650], # Tongass
        [13.1989, 75.4836],   # Western Ghats
        [17.2433, -89.1477],  # Central American
        [-32.7131, 151.5613]  # Eastern Australian
    ]
    
    # Create metrics for each region
    np.random.seed(42)  # For reproducible results
    
    data = {
        'region': regions,
        'latitude': [coord[0] for coord in coordinates],
        'longitude': [coord[1] for coord in coordinates],
        'forest_cover_percent': np.random.uniform(30, 95, len(regions)),
        'health_index': np.random.uniform(4, 10, len(regions)),
        'deforestation_rate': np.random.uniform(0.1, 2.5, len(regions)),
        'biodiversity_index': np.random.uniform(5, 9.5, len(regions)),
        'carbon_storage': np.random.uniform(50, 200, len(regions)),
        'protected_area_percent': np.random.uniform(10, 60, len(regions)),
        'risk_level': np.random.choice(['Low', 'Medium', 'High', 'Critical'], len(regions))
    }
    
    # Adjust some values to match the named regions more realistically
    # Amazon data - generally good health but high deforestation
    data['forest_cover_percent'][0] = 82.5
    data['health_index'][0] = 7.8
    data['deforestation_rate'][0] = 1.2
    data['risk_level'][0] = 'High'
    
    # Borneo - high deforestation pressure
    data['forest_cover_percent'][1] = 71.3
    data['health_index'][1] = 6.2
    data['deforestation_rate'][1] = 1.7
    data['risk_level'][1] = 'Critical'
    
    # Congo - better protected
    data['forest_cover_percent'][2] = 78.1
    data['health_index'][2] = 8.1
    data['deforestation_rate'][2] = 0.5
    data['risk_level'][2] = 'Medium'
    
    return pd.DataFrame(data)


def create_global_health_map(forest_data):
    """
    Create an interactive global map showing forest health indicators.
    
    Parameters:
    -----------
    forest_data : pd.DataFrame
        DataFrame containing forest health data for different regions
    
    Returns:
    --------
    folium.Map
        Interactive map with forest health indicators
    """
    # Create a base map centered at a neutral global position
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
    
    # Add a dark/light tile layer option
    folium.TileLayer('CartoDB dark_matter', name='Dark Map').add_to(m)
    folium.TileLayer('OpenStreetMap', name='Light Map').add_to(m)
    
    # Create a marker cluster group
    marker_cluster = MarkerCluster(name="Forest Regions").add_to(m)
    
    # Create a heatmap of deforestation rates
    heat_data = [[row.latitude, row.longitude, row.deforestation_rate] for _, row in forest_data.iterrows()]
    HeatMap(heat_data, name="Deforestation Intensity", radius=35, blur=20).add_to(m)
    
    # Function to determine marker color based on health index
    def get_color(health_index):
        if health_index >= 8.0:
            return '#4CAF50'  # Green for good health
        elif health_index >= 6.5:
            return '#CDDC39'  # Lime-yellow for moderate health
        elif health_index >= 5.0:
            return '#FFC107'  # Amber for concerning health
        else:
            return '#F44336'  # Red for poor health
    
    # Add markers for each forest region with popups containing detailed information
    for _, row in forest_data.iterrows():
        html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h3 style="color: #4CAF50; margin-bottom: 5px;">{row.region}</h3>
            <div style="height: 2px; background-color: #E0E0E0; margin: 5px 0;"></div>
            <div style="margin: 5px 0;"><b>Forest Cover:</b> {row.forest_cover_percent:.1f}%</div>
            <div style="margin: 5px 0;"><b>Health Index:</b> {row.health_index:.1f}/10</div>
            <div style="margin: 5px 0;"><b>Deforestation Rate:</b> {row.deforestation_rate:.2f}% annually</div>
            <div style="margin: 5px 0;"><b>Biodiversity Index:</b> {row.biodiversity_index:.1f}/10</div>
            <div style="margin: 5px 0;"><b>Carbon Storage:</b> {row.carbon_storage:.1f} tons/hectare</div>
            <div style="margin: 5px 0;"><b>Protected Area:</b> {row.protected_area_percent:.1f}%</div>
            <div style="margin: 5px 0;"><b>Risk Level:</b> <span style="color: {
                '#4CAF50' if row.risk_level == 'Low' else 
                '#FFC107' if row.risk_level == 'Medium' else 
                '#FF9800' if row.risk_level == 'High' else '#F44336'
            };">{row.risk_level}</span></div>
        </div>
        """
        
        iframe = folium.IFrame(html=html, width=220, height=250)
        popup = folium.Popup(iframe, max_width=220)
        
        folium.Marker(
            location=[row.latitude, row.longitude],
            popup=popup,
            tooltip=row.region,
            icon=folium.Icon(color='green', icon='tree', prefix='fa')
        ).add_to(marker_cluster)
    
    # Add a choropleth map for country-level forest cover (would use real data)
    # This is a simplified example - in real implementation, you would use actual country GeoJSON data

    # Add layer control
    folium.LayerControl(position='bottomright').add_to(m)
    
    return m


def global_forest_health_section():
    """Display an interactive global map of forest health indicators."""
    # Create a header
    st.markdown("# Global Forest Health Map")
    st.markdown("""
    Explore the health of forest regions around the world. This interactive map provides 
    indicators of forest health, including forest cover, deforestation rates, biodiversity, 
    and conservation status.
    """)
    
    # Add instructions on how to use the map
    with st.expander("How to Use This Map"):
        st.markdown("""
        - **Zoom and Pan**: Use the mouse wheel to zoom in/out and click and drag to pan across the map.
        - **Click on Markers**: Click on any forest region marker to see detailed health metrics.
        - **Layer Toggle**: Use the layer control in the bottom right to switch between different views.
        - **Cluster Expansion**: Click on marker clusters to expand and see individual forest regions.
        """)
    
    # Load the forest health data
    forest_data = load_forest_health_data()
    
    # Create two columns - one for the map, one for controls and stats
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Create the map
        m = create_global_health_map(forest_data)
        
        # Display the map
        st_folium(m, width=800, height=600, returned_objects=[])
    
    with col2:
        # Add filter controls
        st.markdown("### Filter Regions")
        health_threshold = st.slider("Minimum Health Index", 
                               min_value=4.0, 
                               max_value=10.0, 
                               value=5.0, 
                               step=0.5)
        
        deforestation_threshold = st.slider("Maximum Deforestation Rate", 
                                     min_value=0.1, 
                                     max_value=3.0, 
                                     value=2.0, 
                                     step=0.1)
        
        selected_risk = st.multiselect("Risk Levels", 
                                 options=['Low', 'Medium', 'High', 'Critical'],
                                 default=['Low', 'Medium', 'High', 'Critical'])
        
        # Filter the data based on user selections
        filtered_data = forest_data[
            (forest_data['health_index'] >= health_threshold) & 
            (forest_data['deforestation_rate'] <= deforestation_threshold) &
            (forest_data['risk_level'].isin(selected_risk))
        ]
        
        st.markdown(f"### Showing {len(filtered_data)} of {len(forest_data)} regions")
        
        # Display key stats
        st.markdown("### Global Forest Stats")
        avg_health = forest_data['health_index'].mean()
        avg_deforestation = forest_data['deforestation_rate'].mean()
        total_protected = (forest_data['forest_cover_percent'] * forest_data['protected_area_percent'] / 100).sum() / forest_data['forest_cover_percent'].sum()
        
        st.metric("Average Health Index", f"{avg_health:.1f}/10")
        st.metric("Average Deforestation Rate", f"{avg_deforestation:.2f}% per year", delta=f"{avg_deforestation - 0.5:.2f}%", delta_color="inverse")
        st.metric("Protected Forest Area", f"{total_protected:.1f}%")
        
        # Show regions at highest risk
        st.markdown("### Regions at Highest Risk")
        highest_risk = forest_data.sort_values('deforestation_rate', ascending=False).head(3)
        for _, row in highest_risk.iterrows():
            st.markdown(f"""
            <div style="padding: 10px; background-color: {'rgba(244, 67, 54, 0.1)' if row.risk_level == 'Critical' else 'rgba(255, 152, 0, 0.1)'}; border-radius: 5px; margin-bottom: 5px;">
                <b>{row.region}</b>: Deforestation rate of {row.deforestation_rate:.2f}% annually
            </div>
            """, unsafe_allow_html=True)
    
    # Additional data and comparisons section
    st.markdown("## Regional Comparisons")
    
    # Create tabs for different comparison views
    tabs = st.tabs(["Forest Cover", "Deforestation Rates", "Health Indices", "Biodiversity"])
    
    with tabs[0]:
        chart_data = forest_data.sort_values('forest_cover_percent', ascending=False)
        st.bar_chart(chart_data.set_index('region')['forest_cover_percent'], height=400, use_container_width=True)
        
    with tabs[1]:
        chart_data = forest_data.sort_values('deforestation_rate', ascending=False)
        st.bar_chart(chart_data.set_index('region')['deforestation_rate'], height=400, use_container_width=True)
        
    with tabs[2]:
        chart_data = forest_data.sort_values('health_index', ascending=False)
        st.bar_chart(chart_data.set_index('region')['health_index'], height=400, use_container_width=True)
        
    with tabs[3]:
        chart_data = forest_data.sort_values('biodiversity_index', ascending=False)
        st.bar_chart(chart_data.set_index('region')['biodiversity_index'], height=400, use_container_width=True)

    # Methodologies and data sources section
    with st.expander("Methodology and Data Sources"):
        st.markdown("""
        ### Indicators Explanation
        
        This map uses several indicators to assess forest health:
        
        - **Forest Cover Percentage**: The percentage of an area covered by forest.
        - **Health Index**: A composite score (1-10) based on forest density, canopy integrity, and ecosystem health.
        - **Deforestation Rate**: Annual percentage of forest loss.
        - **Biodiversity Index**: A measure (1-10) of species diversity and ecosystem richness.
        - **Carbon Storage**: Estimated carbon stored per hectare in tons.
        - **Protected Area Percentage**: Percentage of the forest under legal protection.
        - **Risk Level**: Overall assessment of the forest's vulnerability.
        
        ### Data Sources
        
        In a production environment, this tool would use data from:
        
        - Global Forest Watch
        - NASA Earth Observations
        - UN Food and Agriculture Organization (FAO)
        - World Resources Institute
        - National forest inventories
        - Local conservation organizations
        
        Data is refreshed quarterly to provide up-to-date assessments of forest health.
        """)