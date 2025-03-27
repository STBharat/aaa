import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_extras.colored_header import colored_header
from streamlit_extras.card import card

def statistics_section():
    """Display statistics and metrics about deforestation."""
    
    # Use colored_header instead of standard header for better visibility
    colored_header(
        label="Deforestation Statistics & Metrics",
        description="Comprehensive metrics about forest loss and environmental impact",
        color_name="green-70"
    )
    
    # Default to Amazon Rainforest if no location is selected
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = "Amazon Rainforest"
    
    # Create a location selector to allow users to change the data view
    location_options = ["Amazon Rainforest", "Borneo", "Congo Basin"]
    selected_location = st.selectbox(
        "Select a region to analyze:", 
        options=location_options,
        index=location_options.index(st.session_state.selected_location)
    )
    
    # Update session state with selected location
    st.session_state.selected_location = selected_location
    
    # Display top metrics in cards
    st.markdown("### Key Deforestation Indicators")
    
    # Generate metrics based on selected location
    if selected_location == "Amazon Rainforest":
        annual_rate = 0.49
        total_loss = 17.1
        remaining = 82.9
        critical_areas = 37
    elif selected_location == "Borneo":
        annual_rate = 0.62
        total_loss = 25.3
        remaining = 74.7
        critical_areas = 29
    else:  # Congo Basin
        annual_rate = 0.31
        total_loss = 10.2
        remaining = 89.8
        critical_areas = 18
    
    # Display metric cards in a 4-column layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        card(
            title="Annual Loss Rate",
            text=f"{annual_rate}%\nper year",
            image=None,
            styles={
                "card": {
                    "width": "100%",
                    "height": "130px",
                    "border-radius": "10px",
                    "box-shadow": "0 4px 10px rgba(0,0,0,0.1)",
                    "background-color": "#2e7d32",
                },
                "title": {
                    "color": "white",
                    "font-size": "16px",
                },
                "text": {
                    "font-size": "24px",
                    "font-weight": "bold",
                    "color": "white"
                }
            }
        )
    
    with col2:
        card(
            title="Total Forest Loss",
            text=f"{total_loss}%\nsince 2000",
            image=None,
            styles={
                "card": {
                    "width": "100%",
                    "height": "130px",
                    "border-radius": "10px",
                    "box-shadow": "0 4px 10px rgba(0,0,0,0.1)",
                    "background-color": "#d32f2f",
                },
                "title": {
                    "color": "white",
                    "font-size": "16px",
                },
                "text": {
                    "font-size": "24px",
                    "font-weight": "bold",
                    "color": "white"
                }
            }
        )
    
    with col3:
        card(
            title="Forest Remaining",
            text=f"{remaining}%\ncurrent cover",
            image=None,
            styles={
                "card": {
                    "width": "100%",
                    "height": "130px",
                    "border-radius": "10px",
                    "box-shadow": "0 4px 10px rgba(0,0,0,0.1)",
                    "background-color": "#1976d2",
                },
                "title": {
                    "color": "white",
                    "font-size": "16px",
                },
                "text": {
                    "font-size": "24px",
                    "font-weight": "bold",
                    "color": "white"
                }
            }
        )
    
    with col4:
        card(
            title="Critical Areas",
            text=f"{critical_areas}\nhotspots",
            image=None,
            styles={
                "card": {
                    "width": "100%",
                    "height": "130px",
                    "border-radius": "10px",
                    "box-shadow": "0 4px 10px rgba(0,0,0,0.1)",
                    "background-color": "#ff9800",
                },
                "title": {
                    "color": "white",
                    "font-size": "16px",
                },
                "text": {
                    "font-size": "24px",
                    "font-weight": "bold",
                    "color": "white"
                }
            }
        )
    
    # Add a separator
    st.markdown("---")
    
    # Main content in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Deforestation by Land Use")
        
        # Generate sample data based on selected location
        if selected_location == "Amazon Rainforest":
            land_use = {
                "Agriculture": 45,
                "Cattle Ranching": 30,
                "Logging": 15,
                "Mining": 5,
                "Infrastructure": 5
            }
        elif selected_location == "Borneo":
            land_use = {
                "Palm Oil Plantations": 55,
                "Logging": 20,
                "Agriculture": 15,
                "Mining": 7,
                "Urban Development": 3
            }
        else:  # Congo Basin
            land_use = {
                "Subsistence Farming": 35,
                "Commercial Logging": 30,
                "Fuelwood Collection": 20,
                "Mining": 10,
                "Infrastructure": 5
            }
        
        # Create pie chart for land use with better styling
        land_use_df = pd.DataFrame({
            'Land Use': land_use.keys(),
            'Percentage': land_use.values()
        })
        
        fig = px.pie(
            land_use_df,
            values='Percentage',
            names='Land Use',
            title=f'Deforestation Drivers in {selected_location}',
            color_discrete_sequence=px.colors.qualitative.G10,
            hole=0.4
        )
        
        # Improve styling
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            title_font=dict(size=18, family="Arial", color="#2e7d32"),
            font=dict(family="Arial"),
            margin=dict(t=50, b=70, l=40, r=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=2))
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Environmental Impact")
        
        # Create metrics for environmental impact
        if selected_location == "Amazon Rainforest":
            carbon_emissions = 120
            biodiversity_loss = 85
            soil_erosion = 70
        elif selected_location == "Borneo":
            carbon_emissions = 150
            biodiversity_loss = 90
            soil_erosion = 75
        else:  # Congo Basin
            carbon_emissions = 90
            biodiversity_loss = 65
            soil_erosion = 50
            
        # Create a more engaging metrics display
        env_impact_data = [
            {"name": "Carbon Emissions", "value": f"{carbon_emissions}M", "unit": "tons", "change": "+1.5%", "color": "#d32f2f"},
            {"name": "Biodiversity Loss", "value": f"{biodiversity_loss}", "unit": "species", "change": "+2.3%", "color": "#ff9800"},
            {"name": "Soil Erosion", "value": f"{soil_erosion}K", "unit": "hectares", "change": "+0.8%", "color": "#795548"}
        ]
        
        # Create metrics with styled cards
        for i, impact in enumerate(env_impact_data):
            st.markdown(
                f"""
                <div style="padding: 15px; border-left: 5px solid {impact['color']}; 
                           background-color: rgba({int(impact['color'][1:3], 16)}, 
                                                 {int(impact['color'][3:5], 16)}, 
                                                 {int(impact['color'][5:7], 16)}, 0.1); 
                           border-radius: 4px; margin-bottom: 10px;">
                    <span style="font-size: 14px; color: #555;">{impact['name']}</span>
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-size: 24px; font-weight: bold; color: {impact['color']};">
                            {impact['value']} <span style="font-size: 14px;">{impact['unit']}</span>
                        </span>
                        <span style="color: #d32f2f; font-weight: bold;">
                            {impact['change']}
                        </span>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    with col2:
        st.markdown("### Historical Deforestation Rates")
        
        # Create sample historical data
        regions = {
            "Amazon Rainforest": {
                "1990s": 2.5,
                "2000s": 3.2,
                "2010s": 2.8,
                "2020s": 3.6
            },
            "Borneo": {
                "1990s": 3.8,
                "2000s": 4.5,
                "2010s": 4.0,
                "2020s": 3.7
            },
            "Congo Basin": {
                "1990s": 1.2,
                "2000s": 1.5,
                "2010s": 1.8,
                "2020s": 2.0
            }
        }
        
        # Create the historical data for the selected location
        decades = list(regions[selected_location].keys())
        rates = list(regions[selected_location].values())
        
        historical_df = pd.DataFrame({
            'Decade': decades,
            'Deforestation Rate (%)': rates
        })
        
        # Create improved bar chart
        fig = px.bar(
            historical_df,
            x='Decade',
            y='Deforestation Rate (%)',
            title=f'Historical Deforestation Rates in {selected_location}',
            color='Deforestation Rate (%)',
            color_continuous_scale=[(0, "#c8e6c9"), (0.5, "#66bb6a"), (1, "#2e7d32")],
            height=350
        )
        
        # Add trend line
        fig.add_trace(
            go.Scatter(
                x=decades,
                y=rates,
                mode='lines+markers',
                name='Trend',
                line=dict(color='rgba(255, 87, 34, 0.8)', width=3),
                marker=dict(size=8, color='rgba(255, 87, 34, 0.8)')
            )
        )
        
        # Improved styling
        fig.update_layout(
            title_font=dict(size=18, family="Arial", color="#2e7d32"),
            font=dict(family="Arial"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=50, b=40, l=40, r=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Global Comparison")
        
        # Sample global comparison data
        global_data = {
            "Amazon": 3.6,
            "Borneo": 3.7,
            "Congo Basin": 2.0,
            "Southeast Asia": 3.2,
            "Central America": 2.8
        }
        
        global_df = pd.DataFrame({
            'Region': list(global_data.keys()),
            'Current Deforestation Rate (%)': list(global_data.values())
        })
        
        # Create improved horizontal bar chart for global comparison
        fig = px.bar(
            global_df,
            y='Region',
            x='Current Deforestation Rate (%)',
            title='Global Deforestation Rate Comparison',
            orientation='h',
            height=350,
            color='Current Deforestation Rate (%)',
            color_continuous_scale=[(0, "#c8e6c9"), (0.5, "#66bb6a"), (1, "#2e7d32")]
        )
        
        # Highlight the current region
        highlight_region = "Amazon" if selected_location == "Amazon Rainforest" else selected_location
        
        fig.update_traces(
            marker=dict(
                line=dict(
                    color=['rgba(255,152,0,1)' if region == highlight_region else 'rgba(0,0,0,0)' 
                           for region in global_df['Region']],
                    width=3
                )
            )
        )
        
        fig.update_layout(
            title_font=dict(size=18, family="Arial", color="#2e7d32"),
            font=dict(family="Arial"),
            margin=dict(t=50, b=40, l=40, r=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
            
    # Add a styled separator
    st.markdown("""
    <div style="height: 3px; background: linear-gradient(90deg, #2e7d32, rgba(46, 125, 50, 0.3), transparent); margin: 25px 0 30px 0;"></div>
    """, unsafe_allow_html=True)
    
    # Conservation efforts section with better styling
    st.markdown("### Conservation Efforts and Recommendations")
    
    if selected_location == "Amazon Rainforest":
        conservation_efforts = [
            "Strengthening protected area management",
            "Supporting indigenous land rights",
            "Promoting sustainable agriculture practices",
            "Implementing zero-deforestation supply chain commitments"
        ]
        success_story = "Brazil reduced Amazon deforestation by over 80% between 2004 and 2012 through improved monitoring and enforcement."
        
    elif selected_location == "Borneo":
        conservation_efforts = [
            "Developing sustainable palm oil certification",
            "Restoring degraded peatlands",
            "Creating wildlife corridors between forest fragments",
            "Supporting community-based forest management"
        ]
        success_story = "Heart of Borneo initiative has protected over 22 million hectares of forest across Indonesia, Malaysia, and Brunei."
        
    else:  # Congo Basin
        conservation_efforts = [
            "Improving forest governance and transparency",
            "Developing alternative livelihoods for forest-dependent communities",
            "Expanding protected area networks",
            "Addressing illegal logging through certification schemes"
        ]
        success_story = "Central African Forest Initiative (CAFI) has mobilized over $500 million for forest conservation in the region."
    
    # Create a styled layout for conservation section
    col3, col4 = st.columns([3, 2])
    
    with col3:
        st.markdown("#### Recommended Conservation Strategies")
        
        # Create a more visually engaging list of conservation efforts
        for i, effort in enumerate(conservation_efforts):
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom: 15px; 
                           background-color: rgba(46, 125, 50, 0.05); 
                           padding: 15px; border-radius: 8px;">
                    <div style="background-color: #2e7d32; color: white; 
                               border-radius: 50%; width: 28px; height: 28px; 
                               display: flex; justify-content: center; 
                               align-items: center; margin-right: 15px; 
                               font-weight: bold;">{i+1}</div>
                    <div>{effort}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
                
    with col4:
        st.markdown("#### Success Story")
        st.markdown(
            f"""
            <div style="background-color: rgba(25, 118, 210, 0.1); 
                       border-left: 4px solid #1976d2; 
                       padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                <div style="font-style: italic; margin-bottom: 10px;">"{success_story}"</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown("#### Additional Resources")
        
        # Add styled resource links
        resources = [
            {"name": "Global Forest Watch", "url": "https://www.globalforestwatch.org/", "icon": "🌎"},
            {"name": "Deforestation Monitoring Tools", "url": "https://www.wri.org/", "icon": "🔍"},
            {"name": "Conservation International", "url": "https://www.conservation.org/", "icon": "🌿"}
        ]
        
        for resource in resources:
            st.markdown(
                f"""
                <a href="{resource['url']}" target="_blank" style="display: block; text-decoration: none; 
                          color: inherit; margin-bottom: 10px; padding: 10px; 
                          border-radius: 4px; background-color: rgba(46, 125, 50, 0.05);">
                    <div style="display: flex; align-items: center;">
                        <div style="font-size: 20px; margin-right: 10px;">{resource['icon']}</div>
                        <div>{resource['name']}</div>
                    </div>
                </a>
                """, 
                unsafe_allow_html=True
            )
    
    # Add a timestamp for the statistics with better styling
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: right; color: #888; font-size: 0.8em; margin-top: 20px;">
            Statistics generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        """, 
        unsafe_allow_html=True
    )
