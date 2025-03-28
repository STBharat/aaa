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
    
    <script>
        // Wait for content to load before hiding loader
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                document.getElementById('forest-loader').classList.add('hidden');
            }, 1500);
        });
    </script>
    """
    
    st.markdown(loader_html, unsafe_allow_html=True)


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
    # Show loading animation
    loader_html = """
    <div class="forest-loader-container" id="nav-loader">
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
            
            <div class="loading-text">Exploring the Forest...</div>
        </div>
    </div>
    """
    
    st.markdown(loader_html, unsafe_allow_html=True)
    
    # Use JavaScript for smooth transition
    js = f"""
    <script>
        document.getElementById('nav-loader').style.opacity = '1';
        document.getElementById('nav-loader').style.pointerEvents = 'auto';
        
        setTimeout(function() {{
            window.location.href = "/{new_page}";
        }}, {int(delay * 1000)});
    </script>
    """
    
    st.markdown(js, unsafe_allow_html=True)
    

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
    Add a subtle falling leaves animation in the background.
    """
    leaves_html = """
    <style>
    .falling-leaf {
        position: fixed;
        width: 20px;
        height: 20px;
        background-color: rgba(76, 175, 80, 0.6);
        clip-path: ellipse(50% 100% at 50% 50%);
        animation: falling linear infinite;
        z-index: -1;
    }
    
    @keyframes falling {
        0% {
            transform: translate(0, -10%) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        100% {
            transform: translate(100px, 100vh) rotate(360deg);
            opacity: 0;
        }
    }
    </style>
    
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const container = document.body;
        const leafCount = 8;
        
        for (let i = 0; i < leafCount; i++) {
            const leaf = document.createElement('div');
            leaf.className = 'falling-leaf';
            
            // Randomize leaf properties
            const size = Math.random() * 10 + 10; // between 10-20px
            const left = Math.random() * 100; // 0-100% of screen width
            const duration = Math.random() * 10 + 10; // between 10-20s
            const delay = Math.random() * 15; // 0-15s delay
            const rotation = Math.random() * 360; // random initial rotation
            
            leaf.style.width = `${size}px`;
            leaf.style.height = `${size}px`;
            leaf.style.left = `${left}%`;
            leaf.style.animationDuration = `${duration}s`;
            leaf.style.animationDelay = `${delay}s`;
            leaf.style.transform = `rotate(${rotation}deg)`;
            
            // Add a slight color variation
            const hue = 100 + Math.random() * 40; // green hue variation
            leaf.style.backgroundColor = `hsla(${hue}, 80%, 40%, 0.6)`;
            
            container.appendChild(leaf);
        }
    });
    </script>
    """
    
    st.markdown(leaves_html, unsafe_allow_html=True)