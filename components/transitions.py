import streamlit as st
import time

def create_forest_loader():
    """
    Creates a forest-themed loading screen with animations.
    Call this at the beginning of each page to show a loading animation.
    """
    loader_html = """
    <div class="forest-loader-container" id="forest-loader">
        <div class="forest-scene">
            <div class="forest-ground"></div>
            
            <div class="tree">
                <div class="tree-trunk"></div>
                <div class="tree-top">
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                </div>
            </div>
            
            <div class="tree">
                <div class="tree-trunk"></div>
                <div class="tree-top">
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                </div>
            </div>
            
            <div class="tree">
                <div class="tree-trunk"></div>
                <div class="tree-top">
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                </div>
            </div>
            
            <div class="cloud"></div>
            <div class="cloud"></div>
            
            <div class="loading-text">Loading Forest Data...</div>
        </div>
    </div>
    
    <style>
    /* Auto-hide the loader after animation completes */
    .forest-loader-container {
        animation: fadeOutLoader 2s forwards;
        animation-delay: 1.5s;
    }
    
    @keyframes fadeOutLoader {
        from { opacity: 1; }
        to { opacity: 0; visibility: hidden; }
    }
    </style>
    """
    
    # Use a container to limit the scope of the animation
    container = st.container()
    container.markdown(loader_html, unsafe_allow_html=True)


def apply_page_transition():
    """
    Applies a smooth transition animation to the page content.
    This function should be called at the beginning of each page 
    after create_forest_loader() to wrap all content in a transition animation.
    """
    # Start transition container
    st.markdown('<div class="animated-content">', unsafe_allow_html=True)
    
    # Store that we've started a transition container
    if 'transition_started' not in st.session_state:
        st.session_state.transition_started = True


def end_page_transition():
    """
    Closes the transition animation container.
    Call this at the end of a page if needed.
    """
    if 'transition_started' in st.session_state and st.session_state.transition_started:
        st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.transition_started = False


def transition_between_pages(new_page, delay=0.8):
    """
    Create a smooth transition when navigating between pages.
    
    Parameters:
    -----------
    new_page : str
        The name of the page to navigate to
    delay : float
        Delay in seconds before navigation
    """
    # Instead of using JavaScript navigation, use Streamlit's state management
    # Show a loading message
    with st.spinner(f"Navigating to {new_page}..."):
        # Create a visually appealing animation
        placeholder = st.empty()
        placeholder.markdown("""
        <div style="display: flex; justify-content: center; margin: 20px 0;">
            <div style="text-align: center;">
                <div style="font-size: 20px; color: #4CAF50; margin-bottom: 10px;">
                    <i class="fas fa-tree"></i> Exploring the Forest...
                </div>
                <div style="width: 100%; height: 4px; background-color: #e0e0e0; border-radius: 2px; overflow: hidden;">
                    <div class="progress-bar" style="width: 0; height: 100%; background-color: #4CAF50;"></div>
                </div>
            </div>
        </div>
        
        <style>
        @keyframes progress {
            0% { width: 0; }
            100% { width: 100%; }
        }
        .progress-bar {
            animation: progress 0.8s ease-in-out forwards;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Brief delay for visual effect
        time.sleep(delay)
        
        # Update session state to navigate to the new page
        st.session_state.page = new_page
        
        # Remove the placeholder
        placeholder.empty()
    

def page_loading_animation(message="Loading data..."):
    """
    Display a forest-themed loading animation during data processing.
    Use this within a page when loading heavy data.
    
    Parameters:
    -----------
    message : str
        The loading message to display
    
    Returns:
    --------
    placeholder : st.empty
        The placeholder containing the animation that can be cleared
    """
    placeholder = st.empty()
    
    animation_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; margin: 20px 0;">
        <div class="forest-scene" style="width: 150px; height: 150px;">
            <div class="forest-ground"></div>
            
            <div class="tree">
                <div class="tree-trunk"></div>
                <div class="tree-top">
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                </div>
            </div>
            
            <div class="tree">
                <div class="tree-trunk"></div>
                <div class="tree-top">
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                    <div class="leaf"></div>
                </div>
            </div>
            
            <div class="cloud"></div>
            
            <div class="loading-text" style="position: relative; margin-top: 30px; color: var(--text-color);">
                {message}
            </div>
        </div>
    </div>
    """
    
    placeholder.markdown(animation_html, unsafe_allow_html=True)
    return placeholder


def falling_leaves_animation():
    """
    Add a subtle falling leaves animation in the background using CSS only.
    This version avoids JavaScript DOM manipulation which can cause issues.
    """
    # Generate pre-defined leaves with CSS animations
    leaves_html = """
    <style>
    /* Pre-defined falling leaf animations with pure CSS */
    .leaf-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    
    .falling-leaf {
        position: absolute;
        width: 20px;
        height: 20px;
        background-color: rgba(76, 175, 80, 0.6);
        clip-path: ellipse(50% 100% at 50% 50%);
        z-index: -1;
    }
    
    /* Create multiple pre-defined leaves with different animations */
    .leaf-1 {
        left: 15%;
        animation: falling1 15s linear infinite;
        animation-delay: 0s;
        width: 15px;
        height: 15px;
        background-color: rgba(76, 175, 80, 0.5);
    }
    
    .leaf-2 {
        left: 35%;
        animation: falling2 12s linear infinite;
        animation-delay: 1.5s;
        width: 22px;
        height: 22px;
        background-color: rgba(86, 185, 90, 0.5);
    }
    
    .leaf-3 {
        left: 55%;
        animation: falling3 18s linear infinite;
        animation-delay: 3s;
        width: 18px;
        height: 18px;
        background-color: rgba(56, 155, 60, 0.5);
    }
    
    .leaf-4 {
        left: 75%;
        animation: falling4 14s linear infinite;
        animation-delay: 4.5s;
        width: 12px;
        height: 12px;
        background-color: rgba(96, 195, 100, 0.5);
    }
    
    .leaf-5 {
        left: 90%;
        animation: falling5 16s linear infinite;
        animation-delay: 6s;
        width: 20px;
        height: 20px;
        background-color: rgba(66, 165, 70, 0.5);
    }
    
    .leaf-6 {
        left: 25%;
        animation: falling1 17s linear infinite;
        animation-delay: 7.5s;
        width: 16px;
        height: 16px;
        background-color: rgba(86, 185, 90, 0.5);
    }
    
    .leaf-7 {
        left: 65%;
        animation: falling2 13s linear infinite;
        animation-delay: 9s;
        width: 24px;
        height: 24px;
        background-color: rgba(76, 175, 80, 0.5);
    }
    
    .leaf-8 {
        left: 45%;
        animation: falling3 19s linear infinite;
        animation-delay: 10.5s;
        width: 14px;
        height: 14px;
        background-color: rgba(56, 155, 60, 0.5);
    }
    
    /* Different fall paths */
    @keyframes falling1 {
        0% { top: -10%; transform: translateX(0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        100% { top: 100%; transform: translateX(100px) rotate(360deg); opacity: 0; }
    }
    
    @keyframes falling2 {
        0% { top: -10%; transform: translateX(0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        100% { top: 100%; transform: translateX(-120px) rotate(-360deg); opacity: 0; }
    }
    
    @keyframes falling3 {
        0% { top: -10%; transform: translateX(0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        100% { top: 100%; transform: translateX(80px) rotate(720deg); opacity: 0; }
    }
    
    @keyframes falling4 {
        0% { top: -10%; transform: translateX(0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        100% { top: 100%; transform: translateX(-60px) rotate(-720deg); opacity: 0; }
    }
    
    @keyframes falling5 {
        0% { top: -10%; transform: translateX(0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        100% { top: 100%; transform: translateX(140px) rotate(540deg); opacity: 0; }
    }
    </style>
    
    <div class="leaf-container">
        <div class="falling-leaf leaf-1"></div>
        <div class="falling-leaf leaf-2"></div>
        <div class="falling-leaf leaf-3"></div>
        <div class="falling-leaf leaf-4"></div>
        <div class="falling-leaf leaf-5"></div>
        <div class="falling-leaf leaf-6"></div>
        <div class="falling-leaf leaf-7"></div>
        <div class="falling-leaf leaf-8"></div>
    </div>
    """
    
    # Use a container to limit the scope of the animation
    container = st.container()
    container.markdown(leaves_html, unsafe_allow_html=True)