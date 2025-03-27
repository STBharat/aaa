import streamlit as st
import folium
from streamlit_folium import folium_static
import datetime
import pandas as pd
import numpy as np
import json
import random
from streamlit_extras.colored_header import colored_header
from datetime import datetime, timedelta
import time
import folium.plugins

# Import utilities
from utils.mapping import create_map_with_deforestation
from data.sample_coordinates import get_coordinates_for_location

def get_recent_alerts(location, days_back=30):
    """
    Generate simulated recent deforestation alerts.
    In a real app, this would connect to an API like Global Forest Watch.
    
    Parameters:
    -----------
    location : str
        The name of the location
    days_back : int
        Number of days to look back for alerts
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with alert data
    """
    # Get base coordinates for the location
    base_coords = get_coordinates_for_location(location)
    center_lat = base_coords['lat']
    center_lon = base_coords['lon']
    
    # Number of alerts to generate
    num_alerts = random.randint(5, 25)
    
    # Generate random alerts
    alerts = []
    for _ in range(num_alerts):
        # Random date within the last days_back days
        days_ago = random.randint(0, days_back)
        alert_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Random coordinates near the center
        lat_offset = (random.random() - 0.5) * 0.5  # +/- 0.25 degrees
        lon_offset = (random.random() - 0.5) * 0.5  # +/- 0.25 degrees
        
        # Random severity (1-5, with 5 being highest)
        severity = random.randint(1, 5)
        
        # Random area affected (in hectares)
        area = round(random.uniform(0.5, 20.0), 2)
        
        # Random confidence (50-100%)
        confidence = random.randint(50, 100)
        
        alerts.append({
            'date': alert_date,
            'lat': center_lat + lat_offset,
            'lon': center_lon + lon_offset,
            'severity': severity,
            'area_ha': area,
            'confidence': confidence,
            'status': random.choice(['Active', 'Verified', 'Under Investigation'])
        })
    
    # Create DataFrame and sort by date (newest first)
    df = pd.DataFrame(alerts)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date', ascending=False)
    
    return df

def create_alert_map(alerts_df, center_lat, center_lon, zoom=9):
    """
    Create an interactive map with deforestation alerts.
    
    Parameters:
    -----------
    alerts_df : pd.DataFrame
        DataFrame with alert data
    center_lat : float
        Center latitude
    center_lon : float
        Center longitude
    zoom : int
        Initial zoom level
        
    Returns:
    --------
    folium.Map
        Interactive map with alerts
    """
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="OpenStreetMap",
        control_scale=True
    )
    
    # Add Satellite view as a layer
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add Forest Cover layer (simulated)
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Base Map',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Create marker clusters for alerts
    marker_cluster = folium.plugins.MarkerCluster(name="Deforestation Alerts").add_to(m)
    
    # Define severity colors
    severity_colors = {
        1: 'green',
        2: 'blue',
        3: 'orange',
        4: 'darkred',
        5: 'black'
    }
    
    # Add alerts to the map
    for _, alert in alerts_df.iterrows():
        # Create popup content
        popup_content = f"""
        <div style="width: 200px;">
            <h4>Deforestation Alert</h4>
            <p><b>Date:</b> {alert['date'].strftime('%Y-%m-%d')}</p>
            <p><b>Severity:</b> {alert['severity']}/5</p>
            <p><b>Area:</b> {alert['area_ha']} hectares</p>
            <p><b>Confidence:</b> {alert['confidence']}%</p>
            <p><b>Status:</b> {alert['status']}</p>
        </div>
        """
        
        # Create popup
        popup = folium.Popup(popup_content, max_width=300)
        
        # Select marker color based on severity
        color = severity_colors.get(alert['severity'], 'red')
        
        # Add marker
        folium.Marker(
            location=[alert['lat'], alert['lon']],
            popup=popup,
            icon=folium.Icon(color=color, icon='warning-sign', prefix='glyphicon'),
            tooltip=f"Alert: {alert['date'].strftime('%Y-%m-%d')}"
        ).add_to(marker_cluster)
        
        # Add circle with radius proportional to area affected
        folium.Circle(
            location=[alert['lat'], alert['lon']],
            radius=alert['area_ha'] * 50,  # Scale for visibility
            color=color,
            fill=True,
            fill_opacity=0.4,
            weight=2,
            popup=f"Area: {alert['area_ha']} hectares"
        ).add_to(m)
    
    # Add heatmap layer
    heat_data = [[row['lat'], row['lon'], row['severity'] * row['area_ha']] for _, row in alerts_df.iterrows()]
    folium.plugins.HeatMap(
        heat_data,
        radius=15,
        gradient={
            '0.4': 'blue', 
            '0.65': 'yellow', 
            '0.9': 'orange', 
            '1.0': 'red'
        },
        name="Heat Map",
        min_opacity=0.5,
        max_zoom=10
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add fullscreen button
    folium.plugins.Fullscreen(
        position='topleft'
    ).add_to(m)
    
    # Add measure tool
    folium.plugins.MeasureControl(
        position='topleft',
        primary_length_unit='kilometers',
        secondary_length_unit='miles',
        primary_area_unit='hectares',
        secondary_area_unit='acres'
    ).add_to(m)
    
    return m

def realtime_mapping_section():
    """Display real-time mapping of deforestation alerts."""
    colored_header(
        label="Real-Time Deforestation Monitoring",
        description="Monitor forest changes with near real-time alerts",
        color_name="green-70"
    )
    
    st.write("""
    This interactive map displays near real-time deforestation alerts and allows you to monitor 
    forest changes as they're detected by satellite imagery.
    """)
    
    # Add information about the data source (this would be real in a production app)
    with st.expander("About This Data"):
        st.markdown("""
        ### Data Sources
        * **Satellite Data**: Sentinel-2 imagery with 10m resolution
        * **Alert System**: Based on automated detection algorithms
        * **Update Frequency**: Updates would typically occur every 6-8 days depending on cloud cover
        * **Confidence Score**: Indicates reliability of the detected change
        
        In a production environment, this system would integrate with services like:
        * NASA FIRMS (Fire Information for Resource Management System)
        * Global Forest Watch API
        * JRC Global Surface Water Explorer
        """)
    
    # Location selector with 3 options
    col1, col2 = st.columns([3, 1])
    with col1:
        location = st.selectbox(
            "Select Region",
            ["Amazon Rainforest", "Borneo", "Congo Basin"]
        )
    
    # Get coordinates for selected location
    coordinates = get_coordinates_for_location(location)
    center_lat = coordinates['lat']
    center_lon = coordinates['lon']
    
    # Date range selector for alerts
    with col2:
        days_back = st.slider("Days to look back", 1, 90, 30)
    
    # Simulate loading real-time data
    with st.spinner("Loading real-time alert data..."):
        # Simulate a brief delay for realism
        time.sleep(0.5)
        alerts_df = get_recent_alerts(location, days_back)
    
    # Display stats about alerts with custom styling
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container():
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 10px; background-color: #FF5252; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h1 style="margin: 0; font-size: 32px; color: white;">{len(alerts_df)}</h1>
                <p style="margin: 0; color: white;">🚨 Total Alerts</p>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        high_severity = len(alerts_df[alerts_df['severity'] >= 4])
        with st.container():
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 10px; background-color: #B71C1C; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h1 style="margin: 0; font-size: 32px; color: white;">{high_severity}</h1>
                <p style="margin: 0; color: white;">⚠️ High Severity</p>
            </div>
            """, unsafe_allow_html=True)
    with col3:
        total_area = round(alerts_df['area_ha'].sum(), 2)
        with st.container():
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 10px; background-color: #2E7D32; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h1 style="margin: 0; font-size: 32px; color: white;">{total_area} ha</h1>
                <p style="margin: 0; color: white;">🌲 Area Affected</p>
            </div>
            """, unsafe_allow_html=True)
    with col4:
        newest_alert = (datetime.now() - alerts_df['date'].max()).days
        with st.container():
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 10px; background-color: #1565C0; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h1 style="margin: 0; font-size: 32px; color: white;">{newest_alert} days ago</h1>
                <p style="margin: 0; color: white;">📅 Latest Alert</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Create and display map
    st.subheader("Deforestation Alert Map")
    alert_map = create_alert_map(alerts_df, center_lat, center_lon)
    folium_static(alert_map, width=1000, height=600)
    
    # Display alert table
    st.subheader("Recent Alerts")
    
    # Add filtering options
    col1, col2 = st.columns(2)
    with col1:
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=[1, 2, 3, 4, 5],
            default=[1, 2, 3, 4, 5]
        )
    
    with col2:
        status_filter = st.multiselect(
            "Filter by Status",
            options=["Active", "Verified", "Under Investigation"],
            default=["Active", "Verified", "Under Investigation"]
        )
    
    # Apply filters
    filtered_df = alerts_df[
        (alerts_df['severity'].isin(severity_filter)) &
        (alerts_df['status'].isin(status_filter))
    ]
    
    # Format the dataframe for display
    display_df = filtered_df.copy()
    display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
    display_df = display_df.rename(columns={
        'date': 'Date',
        'lat': 'Latitude',
        'lon': 'Longitude',
        'severity': 'Severity (1-5)',
        'area_ha': 'Area (ha)',
        'confidence': 'Confidence (%)',
        'status': 'Status'
    })
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Severity (1-5)': st.column_config.ProgressColumn(
                width="medium",
                min_value=1,
                max_value=5,
            ),
            'Confidence (%)': st.column_config.ProgressColumn(
                width="medium",
                min_value=0,
                max_value=100,
                format="%d%%"
            ),
            'Status': st.column_config.SelectboxColumn(
                width="medium",
                options=["Active", "Verified", "Under Investigation"],
            ),
        }
    )
    
    # Add alert response mechanism
    st.subheader("Alert Response System")
    
    tab1, tab2 = st.tabs(["Report New Alert", "Manage Alerts"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Location Description", placeholder="E.g., 5km north of Rio Branco")
            st.number_input("Estimated Area (hectares)", min_value=0.1, max_value=1000.0, value=5.0, step=0.1)
            st.slider("Confidence Level", 50, 100, 75, 5)
        
        with col2:
            st.date_input("Date Observed", value=datetime.now())
            st.selectbox("Alert Type", ["Clearcutting", "Selective Logging", "Infrastructure Development", "Fire", "Other"])
            st.text_area("Additional Details", placeholder="Describe what you observed...")
        
        st.button("Submit Alert Report", type="primary")
    
    with tab2:
        st.write("In a full implementation, this would allow management of existing alerts with verification status updates, response planning, and team assignment features.")
        
        # Simulated alert management interface
        st.dataframe(
            {
                "ID": [f"ALT-{i+1000}" for i in range(5)],
                "Date": [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)],
                "Location": ["Northern Amazon", "Central Borneo", "Southern Congo", "Eastern Amazon", "Western Borneo"],
                "Status": ["In Progress", "Verified", "Resolved", "Under Investigation", "New"],
                "Team": ["Team A", "Team B", "Team A", "Team C", "Unassigned"]
            },
            use_container_width=True,
            hide_index=True
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Change Status", ["New", "Under Investigation", "In Progress", "Verified", "Resolved"])
        with col2:
            st.selectbox("Assign Team", ["Unassigned", "Team A", "Team B", "Team C", "Team D"])
        with col3:
            st.button("Update Selected Alerts")
        
    # Add export options
    st.download_button(
        label="Download Alert Data (CSV)",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name=f"deforestation_alerts_{location.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )