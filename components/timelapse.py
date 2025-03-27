import streamlit as st
import numpy as np
from PIL import Image
import plotly.express as px
import pandas as pd
from datetime import datetime
import time

def timelapse_section():
    """Display time-lapse view of deforestation changes."""
    
    st.header("Time-Lapse Deforestation View")
    
    if not st.session_state.analysis_complete:
        st.warning("No analysis data available. Please upload an image or select a sample location first.")
        return
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Deforestation Over Time")
        
        # If using a sample location, we have timelapse images
        if st.session_state.selected_location != "Custom Upload" and len(st.session_state.timelapse_images) > 0:
            years = sorted(list(st.session_state.timelapse_images.keys()))
            
            # Create a slider to select the year
            selected_year = st.slider(
                "Select year",
                min_value=min(years),
                max_value=max(years),
                value=min(years),
                step=1
            )
            
            # Display the image for the selected year
            if selected_year in st.session_state.timelapse_images:
                st.image(
                    st.session_state.timelapse_images[selected_year],
                    use_container_width=True,
                    caption=f"Satellite Image from {selected_year}"
                )
            
            # Create an auto-play option
            auto_play = st.checkbox("Auto-play time-lapse")
            
            if auto_play:
                play_speed = st.slider("Playback speed (seconds per frame)", 0.5, 3.0, 1.0, 0.1)
                
                progress_bar = st.progress(0)
                
                for i, year in enumerate(years):
                    # Update progress bar
                    progress = i / (len(years) - 1)
                    progress_bar.progress(progress)
                    
                    # Display image
                    st.image(
                        st.session_state.timelapse_images[year],
                        use_container_width=True,
                        caption=f"Satellite Image from {year}"
                    )
                    
                    time.sleep(play_speed)
                    
                    # Clear output for next frame (except for the last one)
                    if i < len(years) - 1:
                        st.rerun()
                
                progress_bar.progress(1.0)
        else:
            # For custom uploads or if no timelapse data is available
            st.info(
                "Time-lapse data is only available for sample locations. "
                "Please select a sample location from the sidebar to view time-lapse data."
            )
            
            # Show a placeholder image
            if st.session_state.analyzed_image is not None:
                st.image(
                    st.session_state.analyzed_image,
                    use_container_width=True,
                    caption="Current Analysis (Time-lapse not available)"
                )
    
    with col2:
        st.subheader("Deforestation Trend Analysis")
        
        # Generate sample data for trend analysis
        if st.session_state.selected_location != "Custom Upload":
            if st.session_state.selected_location == "Amazon Rainforest":
                years = list(range(2000, 2023))
                forest_cover = [100 - (i * 0.7) for i in range(len(years))]
                annual_loss = [0.5 + (i * 0.02) for i in range(len(years))]
            elif st.session_state.selected_location == "Borneo":
                years = list(range(2000, 2023))
                forest_cover = [100 - (i * 1.1) for i in range(len(years))]
                annual_loss = [0.8 + (i * 0.03) for i in range(len(years))]
            else:  # Congo Basin
                years = list(range(2000, 2023))
                forest_cover = [100 - (i * 0.4) for i in range(len(years))]
                annual_loss = [0.3 + (i * 0.01) for i in range(len(years))]
                
            # Create dataframe for plotting
            df = pd.DataFrame({
                'Year': years,
                'Forest Cover (%)': forest_cover,
                'Annual Loss (%)': annual_loss
            })
            
            # Plot forest cover over time
            fig1 = px.line(
                df, 
                x='Year', 
                y='Forest Cover (%)', 
                title=f'Forest Cover Decline in {st.session_state.selected_location}',
                markers=True
            )
            fig1.update_layout(
                xaxis_title="Year",
                yaxis_title="Remaining Forest Cover (%)",
                yaxis=dict(range=[0, 100])
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # Plot annual deforestation rate
            fig2 = px.bar(
                df, 
                x='Year', 
                y='Annual Loss (%)', 
                title=f'Annual Deforestation Rate in {st.session_state.selected_location}',
                color='Annual Loss (%)',
                color_continuous_scale='Reds'
            )
            fig2.update_layout(
                xaxis_title="Year",
                yaxis_title="Annual Deforestation Rate (%)"
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Add some contextual information
            st.subheader("Key Events")
            
            if st.session_state.selected_location == "Amazon Rainforest":
                events = [
                    {"year": 2004, "event": "Implementation of monitoring systems"},
                    {"year": 2012, "event": "New Forest Code enacted"},
                    {"year": 2019, "event": "Spike in deforestation rates"}
                ]
            elif st.session_state.selected_location == "Borneo":
                events = [
                    {"year": 2005, "event": "Major expansion of palm oil plantations"},
                    {"year": 2015, "event": "Severe forest fires"},
                    {"year": 2020, "event": "New conservation initiatives"}
                ]
            else:  # Congo Basin
                events = [
                    {"year": 2008, "event": "Increase in logging concessions"},
                    {"year": 2016, "event": "Protected area expansions"},
                    {"year": 2021, "event": "New international conservation funding"}
                ]
            
            for event in events:
                st.markdown(f"**{event['year']}**: {event['event']}")
        else:
            st.info("Trend analysis is only available for sample locations.")
