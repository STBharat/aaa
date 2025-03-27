import streamlit as st
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime
import pandas as pd

from utils.mapping import create_map_with_deforestation
from utils.visualization import create_deforestation_heatmap
from data.sample_coordinates import get_coordinates_for_location

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
    analysis_tabs = st.tabs(["Image Comparison", "Deforestation Detection", "Map View"])
    
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
    
    with analysis_tabs[2]:  # Map View tab
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
