import streamlit as st
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.mapping import create_map_with_deforestation
from utils.visualization import create_deforestation_heatmap
from data.sample_coordinates import get_coordinates_for_location
from utils.deforestation_analysis import (
    calculate_detailed_deforestation_metrics,
    compare_to_global_regions,
    analyze_weather_impact,
    create_weather_plots,
    create_deforestation_projection
)

def analysis_section():
    """Display analysis results for deforestation detection."""
    
    st.header("Deforestation Analysis Results")
    
    if not st.session_state.analysis_complete:
        st.warning("No analysis data available. Please upload images or select a sample location first.")
        return
    
    # Check if we have before and after images
    has_before_after = ('before_image' in st.session_state and 
                       'after_image' in st.session_state)
    
    # Create tabs for different views
    analysis_tabs = st.tabs([
        "Image Comparison", 
        "Deforestation Detection", 
        "Detailed Metrics", 
        "Weather Impact",
        "Map View", 
        "Future Projections"
    ])
    
    with analysis_tabs[0]:  # Image Comparison tab
        st.subheader("Before and After Satellite Imagery")
        
        if has_before_after:
            # Side-by-side comparison of before and after
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(
                    st.session_state.before_image,
                    use_container_width=True,
                    caption="Before - Original Forest Coverage"
                )
            
            with col2:
                st.image(
                    st.session_state.after_image,
                    use_container_width=True,
                    caption="After - Current Forest Coverage"
                )
                
            # Add slider for image comparison if available
            st.write("Use the slider below to compare the before and after images:")
            
            # Create a comparison container with embedded HTML for image comparison
            comparison_value = st.slider("Slide to compare", 0, 100, 50, key="image_comparison_slider")
            
            # Get the dimensions of the images
            width = getattr(st.session_state.before_image, 'width', 600)
            height = getattr(st.session_state.before_image, 'height', 450)
            
            # Convert images to base64 for HTML embedding
            import base64
            from io import BytesIO
            
            def get_image_base64(img):
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                return base64.b64encode(buffered.getvalue()).decode()
            
            before_b64 = get_image_base64(st.session_state.before_image)
            after_b64 = get_image_base64(st.session_state.after_image)
            
            # Create image comparison with CSS
            comparison_html = f"""
            <style>
            .img-comp-container {{
              position: relative;
              height: {height}px;
              max-width: 100%;
              margin: 0 auto;
            }}
            .img-comp-before {{
              position: absolute;
              top: 0;
              width: 100%;
              height: 100%;
              border-right: 2px solid #fff;
              overflow: hidden;
              width: {comparison_value}%;
            }}
            .img-comp-after {{
              position: absolute;
              top: 0;
              width: 100%;
              height: 100%;
            }}
            .img-comp-before img, .img-comp-after img {{
              display: block;
              vertical-align: middle;
              max-width: 100%;
              height: auto;
              object-fit: cover;
            }}
            </style>
            <div class="img-comp-container">
              <div class="img-comp-after">
                <img src="data:image/png;base64,{after_b64}" width="100%">
              </div>
              <div class="img-comp-before">
                <img src="data:image/png;base64,{before_b64}" width="100%">
              </div>
            </div>
            """
            
            st.markdown(comparison_html, unsafe_allow_html=True)
            
            # Add explanation of what to look for
            st.info("""
            **What to look for in the comparison:**
            - Areas with reduced green vegetation
            - New cleared patches or roads
            - Expansion of agricultural or developed areas
            - Changes in river courses or water bodies
            """)
            
        else:
            # Only single image available (old functionality)
            st.image(
                st.session_state.uploaded_image, 
                use_container_width=True, 
                caption="Satellite Image"
            )
            st.info("Only one image available. Upload both 'Before' and 'After' images for comparison.")
    
    with analysis_tabs[1]:  # Deforestation Detection tab
        st.subheader("Deforestation Detection Analysis")
        
        if has_before_after:
            # Display both before and after analyzed images
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(
                    st.session_state.before_analyzed if hasattr(st.session_state, 'before_analyzed') else st.session_state.before_image,
                    use_container_width=True,
                    caption="Before - Analyzed Forest Coverage"
                )
            
            with col2:
                st.image(
                    st.session_state.after_analyzed if hasattr(st.session_state, 'after_analyzed') else st.session_state.analyzed_image,
                    use_container_width=True,
                    caption="After - Detected Deforestation"
                )
            
            # Add a difference visualization if available
            st.subheader("Detected Changes")
            st.image(
                st.session_state.analyzed_image,
                use_container_width=True,
                caption="Areas of Deforestation Highlighted"
            )
            
        else:
            # Original functionality for single image
            view_option = st.radio(
                "View:",
                ["Original Image", "Analyzed Image with Deforestation Highlighted"]
            )
            
            if view_option == "Original Image" and st.session_state.uploaded_image is not None:
                st.image(
                    st.session_state.uploaded_image, 
                    use_container_width=True, 
                    caption="Original Satellite Image"
                )
            elif view_option == "Analyzed Image with Deforestation Highlighted" and st.session_state.analyzed_image is not None:
                st.image(
                    st.session_state.analyzed_image, 
                    use_container_width=True, 
                    caption="Deforested Areas Highlighted"
                )

    with analysis_tabs[2]:  # Detailed Metrics tab
        st.subheader("Detailed Deforestation Metrics")
        
        if has_before_after:
            # Calculate time difference (for now, assume 1 year between images)
            time_difference_years = 1
            if 'timelapse_images' in st.session_state:
                years = list(st.session_state.timelapse_images.keys())
                if len(years) >= 2:
                    time_difference_years = years[-1] - years[0]
            
            # Allow user to adjust time difference if needed
            time_difference_years = st.slider(
                "Time difference between images (years)",
                min_value=0.1,
                max_value=10.0,
                value=float(time_difference_years),
                step=0.1
            )
            
            # Calculate detailed metrics
            metrics = calculate_detailed_deforestation_metrics(
                st.session_state.before_image,
                st.session_state.after_image,
                time_difference_years
            )
            
            # Store metrics in session state for other tabs
            st.session_state.deforestation_metrics = metrics
            
            # Create boxes for key metrics with icons
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            
            # Create metric cards
            cols = st.columns(3)
            
            with cols[0]:
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: rgba(76, 175, 80, 0.1); text-align: center; height: 100%;">
                    <h3 style="margin-top: 0;">🌳 Forest Coverage</h3>
                    <p>Before: <b>{metrics['before_coverage']:.1f}%</b></p>
                    <p>After: <b>{metrics['after_coverage']:.1f}%</b></p>
                    <p>Change: <b style="color: {'red' if metrics['absolute_change'] > 0 else 'green'};">
                        {metrics['absolute_change']:.1f}%
                    </b></p>
                </div>
                """, unsafe_allow_html=True)
                
            with cols[1]:
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: rgba(76, 175, 80, 0.1); text-align: center; height: 100%;">
                    <h3 style="margin-top: 0;">📊 Annual Rate</h3>
                    <p>Annual deforestation rate:</p>
                    <h2 style="color: {metrics['severity_color']};">{metrics['annual_rate']:.2f}%</h2>
                    <p>Severity: <b style="color: {metrics['severity_color']};">{metrics['severity']}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
            with cols[2]:
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: rgba(76, 175, 80, 0.1); text-align: center; height: 100%;">
                    <h3 style="margin-top: 0;">🌍 Environmental Impact</h3>
                    <p>Carbon impact: <b>{metrics['carbon_impact_tons']:.1f}</b> tons</p>
                    <p>Biodiversity impact: <b>{metrics['biodiversity_impact']:.1f}/10</b></p>
                    <p>Estimated area: <b>{metrics['estimated_area_hectares']}</b> hectares</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
            
            # Compare to global regions
            st.subheader("Regional Comparison")
            comparisons = compare_to_global_regions(metrics['annual_rate'])
            
            # Create a DataFrame for the comparison
            comparison_data = []
            for region, data in comparisons.items():
                comparison_data.append({
                    "Region": region,
                    "Reference Rate (%)": data['difference'] + metrics['annual_rate'] if data['relation'] == 'lower than' else metrics['annual_rate'] - data['difference'],
                    "Comparison": f"{data['relation']} by {data['difference']:.2f}%",
                    "Status": "Better" if data['relation'] == 'lower than' else "Worse" if data['relation'] == 'higher than' else "Similar"
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            
            # Show the comparison table
            st.dataframe(comparison_df)
            
            # Create a bar chart to visualize the comparison
            global_rates = {
                "Current Site": metrics['annual_rate'],
                "Amazon": 0.9,
                "Borneo": 1.3,
                "Congo": 0.3,
                "Global Average": 0.5
            }
            
            regions = list(global_rates.keys())
            rates = list(global_rates.values())
            
            # Create a DataFrame for the bar chart
            bar_data = pd.DataFrame({
                "Region": regions,
                "Annual Deforestation Rate (%)": rates
            })
            
            # Create the bar chart
            fig = px.bar(
                bar_data, 
                x="Region", 
                y="Annual Deforestation Rate (%)",
                color="Region",
                color_discrete_map={
                    "Current Site": metrics['severity_color'],
                    "Amazon": "#FFC107",
                    "Borneo": "#F44336",
                    "Congo": "#4CAF50",
                    "Global Average": "#2196F3"
                },
                title="Comparison with Global Regions"
            )
            
            fig.update_layout(
                xaxis_title="Region",
                yaxis_title="Annual Deforestation Rate (%)",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Create a radar chart for multi-dimensional comparison
            st.subheader("Multi-dimensional Analysis")
            
            # Create sample data for radar chart
            categories = ['Deforestation Rate', 'Carbon Impact', 'Biodiversity Loss', 'Recovery Potential', 'Protection Status']
            
            # Normalize values to 0-10 scale for radar chart
            current_values = [
                min(10, metrics['annual_rate'] * 5),  # Deforestation Rate
                min(10, metrics['carbon_impact_tons'] / 100),  # Carbon Impact
                metrics['biodiversity_impact'],  # Biodiversity Loss
                max(0, 10 - metrics['annual_rate'] * 3),  # Recovery Potential
                5  # Protection Status (assumed middle value)
            ]
            
            # Reference values for a global average
            reference_values = [5, 5, 5, 5, 5]
            
            # Create radar chart
            radar_fig = go.Figure()
            
            radar_fig.add_trace(go.Scatterpolar(
                r=current_values,
                theta=categories,
                fill='toself',
                name='Current Site',
                line_color=metrics['severity_color']
            ))
            
            radar_fig.add_trace(go.Scatterpolar(
                r=reference_values,
                theta=categories,
                fill='toself',
                name='Global Average',
                line_color='rgba(33, 150, 243, 0.7)'
            ))
            
            radar_fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )
                ),
                showlegend=True,
                title="Multi-dimensional Deforestation Impact Analysis"
            )
            
            st.plotly_chart(radar_fig, use_container_width=True)
            
        else:
            st.info("Please upload both 'Before' and 'After' images to view detailed metrics.")
    
    with analysis_tabs[3]:  # Weather Impact tab
        st.subheader("Weather Impact Analysis")
        
        if has_before_after and hasattr(st.session_state, 'deforestation_metrics'):
            # Get time difference
            time_difference_years = st.session_state.deforestation_metrics['time_difference_years']
            
            # Get the location
            location = st.session_state.selected_location
            if location == "Custom Upload":
                location = st.selectbox(
                    "Select a reference region for weather analysis:",
                    ["Amazon Rainforest", "Borneo", "Congo Basin"]
                )
            
            # Calculate weather impact
            weather_impact = analyze_weather_impact(location, time_difference_years)
            
            # Display weather impact summary
            st.markdown(f"""
            <div style="padding: 20px; border-radius: 10px; background-color: rgba(76, 175, 80, 0.1);">
                <h3 style="margin-top: 0;">Weather Impact Summary</h3>
                <p>Average Temperature: <b>{weather_impact['average_temperature']:.1f}°C</b> 
                   (<span style="color: {'red' if weather_impact['temperature_anomaly'] > 0 else 'green'};">
                   {'+' if weather_impact['temperature_anomaly'] > 0 else ''}{weather_impact['temperature_anomaly']:.1f}°C</span> compared to normal)</p>
                
                <p>Total Precipitation: <b>{weather_impact['total_precipitation']:.0f}mm</b>
                   (<span style="color: {'red' if weather_impact['precipitation_anomaly_percent'] < 0 else 'green'};">
                   {'+' if weather_impact['precipitation_anomaly_percent'] > 0 else ''}{weather_impact['precipitation_anomaly_percent']:.1f}%</span> compared to normal)</p>
                
                <p>Drought Periods: <b>{weather_impact['drought_months']}</b> months</p>
                
                <h4>Impact Assessment: <span style="color: {'red' if weather_impact['weather_impact_level'] == 'High' else 'orange' if weather_impact['weather_impact_level'] == 'Moderate' else 'green'};">
                {weather_impact['weather_impact_level']}</span></h4>
                
                <p><b>Contributing Factors:</b></p>
                <ul>
                    {''.join(f'<li>{factor}</li>' for factor in weather_impact['impact_factors'])}
                </ul>
                
                <p><b>Recommendation:</b> {weather_impact['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create weather plots
            st.subheader("Weather Patterns")
            weather_plots = create_weather_plots(weather_impact)
            
            # Display temperature plot
            st.plotly_chart(weather_plots["temperature_plot"], use_container_width=True)
            
            # Display precipitation plot
            st.plotly_chart(weather_plots["precipitation_plot"], use_container_width=True)
            
            # Show correlation analysis
            st.subheader("Weather-Deforestation Correlation")
            
            # Create a simple correlation explanation
            if weather_impact['weather_impact_level'] == 'High':
                correlation_strength = "strong"
                correlation_color = "red"
                explanation = "The weather patterns show significant anomalies that likely contributed to increased deforestation rates. Extended drought periods and higher temperatures create conditions favorable for forest fires and reduce forest resilience."
            elif weather_impact['weather_impact_level'] == 'Moderate':
                correlation_strength = "moderate"
                correlation_color = "orange"
                explanation = "The weather patterns show some anomalies that may have contributed to deforestation. The relationship is not as pronounced, but still notable."
            else:
                correlation_strength = "weak"
                correlation_color = "green"
                explanation = "Weather patterns appear relatively normal for this region. The observed deforestation is likely more strongly driven by human activities than by climate factors."
            
            st.markdown(f"""
            <div style="padding: 15px; border-radius: 5px; background-color: rgba(33, 150, 243, 0.1);">
                <h4>Weather-Deforestation Correlation: <span style="color: {correlation_color}">{correlation_strength.title()}</span></h4>
                <p>{explanation}</p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.info("Please upload both 'Before' and 'After' images and view Detailed Metrics first to enable weather impact analysis.")
    
    with analysis_tabs[4]:  # Map View tab
        st.subheader("Interactive Map of Deforestation")
        
        coordinates = get_coordinates_for_location(st.session_state.selected_location)
        
        # Create interactive map with deforestation areas
        map_view = create_map_with_deforestation(
            center_lat=coordinates["lat"],
            center_lon=coordinates["lon"],
            zoom=coordinates["zoom"],
            deforested_areas=st.session_state.deforested_areas
        )
        
        folium_static(map_view)
        
        st.markdown("""
        **Map Legend:**
        - <span style='color:red'>⬤</span> High deforestation activity
        - <span style='color:orange'>⬤</span> Moderate deforestation activity
        - <span style='color:yellow'>⬤</span> Low deforestation activity
        - <span style='color:green'>⬤</span> Intact forest area
        """, unsafe_allow_html=True)
    
    with analysis_tabs[5]:  # Future Projections tab
        st.subheader("Future Deforestation Projections")
        
        if has_before_after and hasattr(st.session_state, 'deforestation_metrics'):
            metrics = st.session_state.deforestation_metrics
            
            # Create projections
            years_to_project = st.slider(
                "Years to project into the future",
                min_value=5,
                max_value=50,
                value=20,
                step=5
            )
            
            projections = create_deforestation_projection(metrics, years_to_project)
            
            # Display the projection plot
            st.plotly_chart(projections["projection_plot"], use_container_width=True)
            
            # Display key projection insights
            if metrics['annual_rate'] > 0:
                if projections["years_to_50_percent"] is not None:
                    st.warning(f"⚠️ At the current rate of deforestation ({metrics['annual_rate']:.2f}% per year), **50% of the remaining forest will be lost in approximately {projections['years_to_50_percent']} years**.")
                
                # Show potential conservation impact
                st.subheader("Conservation Impact")
                st.markdown(f"""
                <div style="padding: 15px; border-radius: 5px; background-color: rgba(76, 175, 80, 0.1);">
                    <h4>Impact of Conservation Efforts</h4>
                    <p>If conservation efforts reduce the deforestation rate by 50% (to {metrics['annual_rate']/2:.2f}% per year):</p>
                    <ul>
                        <li>The forest coverage would be <b>{projections["projection_data"]["Improved Conservation (50% reduction)"].iloc[-1]:.1f}%</b> after {years_to_project} years</li>
                        <li>This represents a <b>{projections["projection_data"]["Improved Conservation (50% reduction)"].iloc[-1] - projections["projection_data"]["Current Trend"].iloc[-1]:.1f}%</b> improvement over the current trend</li>
                        <li>The time to 50% forest loss would be extended by approximately <b>{projections["years_to_50_percent"]}+</b> years</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("🎉 Good news! The analysis shows forest regeneration rather than deforestation. The current trend shows a positive rate of change.")
        else:
            st.info("Please upload both 'Before' and 'After' images and view Detailed Metrics first to enable future projections.")
    
    # Add Analysis Summary section
    st.subheader("Analysis Summary")
    
    # Create two columns for statistics
    stats_col1, stats_col2 = st.columns([1, 1])
    
    with stats_col1:
        # Create some sample metrics for the analysis
        if st.session_state.selected_location != "Custom Upload":
            if st.session_state.selected_location == "Amazon Rainforest":
                region = "Amazon Basin"
                country = "Brazil"
                total_area = "5.5 million km²"
                deforested = "17%"
                rate = "0.5%"
            elif st.session_state.selected_location == "Borneo":
                region = "Borneo Island"
                country = "Indonesia/Malaysia"
                total_area = "743,330 km²"
                deforested = "25%"
                rate = "1.3%"
            else:  # Congo Basin
                region = "Congo Basin"
                country = "Democratic Republic of Congo"
                total_area = "3.7 million km²"
                deforested = "10%"
                rate = "0.3%"
        else:
            region = "Custom Region"
            country = "Unknown"
            total_area = "Unknown"
            deforested = "Unknown"
            rate = "Unknown"
        
        metrics_data = {
            "Metric": ["Region", "Country", "Total Forest Area", "Deforested Area", "Annual Deforestation Rate"],
            "Value": [region, country, total_area, deforested, rate]
        }
        
        metrics_df = pd.DataFrame(metrics_data)
        st.table(metrics_df)
    
    with stats_col2:
        st.subheader("Risk Assessment")
        
        # Sample risk assessment based on location
        if st.session_state.selected_location == "Amazon Rainforest":
            risk_level = "High"
            risk_color = "red"
            risk_factors = [
                "Illegal logging operations",
                "Agricultural expansion",
                "Mining activities",
                "Road construction"
            ]
        elif st.session_state.selected_location == "Borneo":
            risk_level = "Very High"
            risk_color = "darkred"
            risk_factors = [
                "Palm oil plantations",
                "Timber extraction",
                "Forest fires",
                "Urban development"
            ]
        elif st.session_state.selected_location == "Congo Basin":
            risk_level = "Medium"
            risk_color = "orange"
            risk_factors = [
                "Subsistence agriculture",
                "Commercial logging",
                "Infrastructure development",
                "Charcoal production"
            ]
        else:
            risk_level = "Unknown"
            risk_color = "gray"
            risk_factors = ["Custom upload - risk factors unknown"]
        
        st.markdown(f"**Risk Level: <span style='color:{risk_color}'>{risk_level}</span>**", unsafe_allow_html=True)
        
        st.write("Contributing factors:")
        for factor in risk_factors:
            st.markdown(f"- {factor}")
    
    # Display heatmap below the stats columns
    st.subheader("Deforestation Heatmap")
    heatmap_fig = create_deforestation_heatmap(st.session_state.selected_location)
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
    # Add a timestamp for the analysis
    st.markdown("---")
    st.caption(f"Analysis timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
