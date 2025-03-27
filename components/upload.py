import streamlit as st
import io
from PIL import Image
import numpy as np
import datetime
from utils.image_processing import process_satellite_image
from utils.mapping import create_map_with_deforestation

def upload_section():
    """Create the upload section for satellite images with before and after comparison."""
    
    # Check if we're in dark mode
    is_dark_mode = 'theme' in st.session_state and st.session_state.theme == 'dark'
    
    # Add custom CSS for file uploader text visibility in dark mode
    if is_dark_mode:
        st.markdown("""
        <style>
        [data-testid="stFileUploadDropzone"] p {
            color: white !important;
        }
        [data-testid="stFileUploadDropzone"] small {
            color: rgba(250, 250, 250, 0.7) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Use a cleaner approach with standard Streamlit components
    st.markdown("""
    <div class="component-section">
        <h2 class="component-title">Upload Satellite Imagery</h2>
        <p>Upload 'before' and 'after' satellite imagery to analyze deforestation patterns.
        The system will process both images and highlight areas where deforestation has been detected between the two timepoints.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a cleaner format display with standard Streamlit components
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background-color: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px; 
                    box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
            <h4 style="margin-top: 0; margin-bottom: 0.7rem; color: #2e7d32; font-size: 1rem;">
                📁 Supported Formats
            </h4>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
            <span style="display: inline-block; background-color: rgba(76, 175, 80, 0.2); 
                        padding: 6px 12px; border-radius: 4px; font-size: 0.85rem;">.jpg</span>
            <span style="display: inline-block; background-color: rgba(76, 175, 80, 0.2); 
                        padding: 6px 12px; border-radius: 4px; font-size: 0.85rem;">.jpeg</span>
            <span style="display: inline-block; background-color: rgba(76, 175, 80, 0.2); 
                        padding: 6px 12px; border-radius: 4px; font-size: 0.85rem;">.png</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px; 
                    box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
            <h4 style="margin-top: 0; margin-bottom: 0.7rem; color: #2e7d32; font-size: 1rem;">
                🔍 Recommended Resolution
            </h4>
            <p style="margin: 0; font-size: 0.9rem;">
                1000×1000 pixels or higher for optimal analysis results
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add custom CSS for radio buttons
    st.markdown("""
    <style>
    div[role="radiogroup"] {
        margin: 1rem 0;
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    div[data-testid="stRadio"] > label {
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #2e7d32;
    }
    div[data-testid="stHorizontalBlock"] {
        background-color: rgba(76, 175, 80, 0.05); 
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    /* Dark mode styles */
    body.dark div[data-testid="stHorizontalBlock"] {
        background-color: rgba(76, 175, 80, 0.1);
    }
    body.dark div[data-testid="stRadio"] > label {
        color: #4caf50;
    }
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        background-color: #f5f5f5;
        border: none !important;
        color: #555;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e8f5e9 !important;
        color: #2e7d32 !important;
        font-weight: 600;
    }
    /* Dark mode tab styling */
    body.dark .stTabs [data-baseweb="tab"] {
        background-color: #333;
        color: #ccc;
    }
    body.dark .stTabs [aria-selected="true"] {
        background-color: rgba(76, 175, 80, 0.3) !important;
        color: #4caf50 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Upload method selection
    upload_method = st.radio(
        "Select upload method:",
        ["Upload your own images", "Use sample imagery"]
    )
    
    if upload_method == "Upload your own images":
        # Create tabs for before and after uploads
        upload_tabs = st.tabs(["Before Image", "After Image", "Comparison Preview"])
        
        with upload_tabs[0]:  # Before Image Tab
            st.subheader("Upload 'Before' Image")
            uploaded_before = st.file_uploader(
                "Choose a satellite image (earlier timepoint)",
                type=["jpg", "jpeg", "png"],
                key="before_uploader"
            )
            
            # Preview of before image
            if uploaded_before is not None:
                try:
                    # Read the uploaded image
                    before_image = Image.open(uploaded_before)
                    st.session_state.before_image = before_image
                    
                    # Display preview
                    st.image(before_image, use_container_width=True, caption="'Before' Image Preview")
                    st.success("'Before' image uploaded successfully!")
                    
                except Exception as e:
                    st.error(f"Error processing 'Before' image: {str(e)}")
            else:
                # Show placeholder for before image
                display_image_placeholder("Upload 'Before' image", is_dark_mode)
        
        with upload_tabs[1]:  # After Image Tab
            st.subheader("Upload 'After' Image")
            uploaded_after = st.file_uploader(
                "Choose a satellite image (later timepoint)",
                type=["jpg", "jpeg", "png"],
                key="after_uploader"
            )
            
            # Preview of after image
            if uploaded_after is not None:
                try:
                    # Read the uploaded image
                    after_image = Image.open(uploaded_after)
                    st.session_state.after_image = after_image
                    
                    # Display preview
                    st.image(after_image, use_container_width=True, caption="'After' Image Preview")
                    st.success("'After' image uploaded successfully!")
                    
                except Exception as e:
                    st.error(f"Error processing 'After' image: {str(e)}")
            else:
                # Show placeholder for after image
                display_image_placeholder("Upload 'After' image", is_dark_mode)
        
        with upload_tabs[2]:  # Comparison Preview Tab
            st.subheader("Compare Before & After Images")
            
            both_images_uploaded = ('before_image' in st.session_state and 
                                  'after_image' in st.session_state)
            
            if both_images_uploaded:
                # Display side by side comparison
                col1, col2 = st.columns(2)
                with col1:
                    st.image(st.session_state.before_image, use_container_width=True, caption="Before")
                with col2:
                    st.image(st.session_state.after_image, use_container_width=True, caption="After")
                
                # Process button
                if st.button("Analyze Deforestation Between Images"):
                    with st.spinner("Analyzing deforestation patterns..."):
                        # Process the before image for reference
                        before_analyzed, _ = process_satellite_image(st.session_state.before_image)
                        st.session_state.before_analyzed = before_analyzed
                        
                        # Process the after image for comparison and detection
                        after_analyzed, deforested_areas = process_satellite_image(st.session_state.after_image)
                        st.session_state.after_analyzed = after_analyzed
                        st.session_state.deforested_areas = deforested_areas
                        
                        # Set uploaded_image to after image for compatibility with other components
                        st.session_state.uploaded_image = st.session_state.after_image
                        st.session_state.analyzed_image = after_analyzed
                        
                        # Mark analysis as complete
                        st.session_state.analysis_complete = True
                        
                        # Display success message
                        st.success("Analysis complete! Navigate to Analysis Results to view detailed findings.")
            else:
                st.info("Please upload both 'Before' and 'After' images to enable comparison and analysis.")
                
                if 'before_image' not in st.session_state:
                    st.warning("'Before' image not yet uploaded.")
                    
                if 'after_image' not in st.session_state:
                    st.warning("'After' image not yet uploaded.")
                
                # Show placeholder for comparison
                display_image_placeholder("Before and After comparison will appear here", is_dark_mode, height=300)
    
    else:  # Sample imagery option
        st.subheader("Sample Imagery")
        
        # Sample options
        sample_options = {
            "Amazon Rainforest (2018-2020)": {"before_year": 2018, "after_year": 2020},
            "Borneo (2019-2021)": {"before_year": 2019, "after_year": 2021},
            "Congo Basin (2017-2019)": {"before_year": 2017, "after_year": 2019}
        }
        
        sample_selection = st.selectbox("Select a sample location and time period", list(sample_options.keys()))
        selected_years = sample_options[sample_selection]
        
        # Display the selected sample information
        st.info(f"This will load sample satellite imagery of {sample_selection.split(' (')[0]} from {selected_years['before_year']} and {selected_years['after_year']}.")
        
        # Button to load the sample
        if st.button("Load Sample Images"):
            with st.spinner(f"Loading sample data for {sample_selection}..."):
                # Generate sample images for demonstration
                width, height = 800, 600
                
                # Base image array with random noise
                base_image_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
                
                # "Before" image - more green to represent more forest
                before_array = np.copy(base_image_array)
                before_array[:, :, 1] = np.clip(before_array[:, :, 1] + 100, 0, 255)  # Enhance green
                before_image = Image.fromarray(before_array)
                
                # "After" image - less green to represent deforestation
                after_array = np.copy(base_image_array)
                after_array[:, :, 1] = np.clip(after_array[:, :, 1] + 50, 0, 255)  # Less green
                # Add some brown patches to simulate cleared land
                mask = np.random.rand(height, width) > 0.8
                after_array[mask, 0] = np.clip(after_array[mask, 0] + 70, 0, 255)  # More red
                after_array[mask, 1] = np.clip(after_array[mask, 1] - 50, 0, 255)  # Less green
                after_image = Image.fromarray(after_array)
                
                # Store the images in session state
                st.session_state.before_image = before_image
                st.session_state.after_image = after_image
                st.session_state.uploaded_image = after_image  # For compatibility with other components
                
                # Process the images
                before_analyzed, _ = process_satellite_image(before_image)
                after_analyzed, deforested_areas = process_satellite_image(after_image)
                
                # Store the processed results
                st.session_state.before_analyzed = before_analyzed
                st.session_state.after_analyzed = after_analyzed
                st.session_state.analyzed_image = after_analyzed
                st.session_state.deforested_areas = deforested_areas
                st.session_state.analysis_complete = True
                
                # Generate timelapse images
                years = list(range(selected_years['before_year'], selected_years['after_year'] + 1))
                st.session_state.timelapse_images = {}
                
                for i, year in enumerate(years):
                    # Interpolate between before and after images to simulate progression
                    progress = i / (len(years) - 1)
                    year_array = (1 - progress) * before_array + progress * after_array
                    year_image = Image.fromarray(year_array.astype(np.uint8))
                    st.session_state.timelapse_images[year] = year_image
                
                # Display success message
                st.success(f"Sample data for {sample_selection} loaded successfully! Navigate to Analysis Results to view details.")
            
            # Show a preview of the loaded samples
            col1, col2 = st.columns(2)
            with col1:
                st.image(before_image, use_container_width=True, 
                         caption=f"Before ({selected_years['before_year']})")
            with col2:
                st.image(after_image, use_container_width=True, 
                         caption=f"After ({selected_years['after_year']})")


def display_image_placeholder(message, is_dark_mode, height=200):
    """Helper function to display a consistent image placeholder."""
    # Determine border and text color based on theme
    border_color = "#555" if is_dark_mode else "#ccc"
    text_color = "#aaa" if is_dark_mode else "#888"
    
    # Show a placeholder with the provided message
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; 
        height: {height}px; border: 2px dashed {border_color}; border-radius: 5px;">
            <p style="color: {text_color};">{message}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
