import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.card import card
import base64
from PIL import Image
from io import BytesIO

def create_svg_icon(icon_type):
    """Generate SVG icons for action cards"""
    if icon_type == "reduce":
        return """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="#4caf50">
            <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,10.5A1.5,1.5 0 0,1 13.5,12A1.5,1.5 0 0,1 12,13.5A1.5,1.5 0 0,1 10.5,12A1.5,1.5 0 0,1 12,10.5M7.5,12A1.5,1.5 0 0,1 9,13.5A1.5,1.5 0 0,1 7.5,15A1.5,1.5 0 0,1 6,13.5A1.5,1.5 0 0,1 7.5,12M16.5,12A1.5,1.5 0 0,1 18,13.5A1.5,1.5 0 0,1 16.5,15A1.5,1.5 0 0,1 15,13.5A1.5,1.5 0 0,1 16.5,12Z" />
        </svg>
        """
    elif icon_type == "support":
        return """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="#2e7d32">
            <path d="M21,10.5H20V8H17V10.5H16.5V7H14V10.5H13.5V5H11V10.5H10.5V8H7.5V10.5H7V7H4V10.5H3A1,1 0 0,0 2,11.5V13.5A1,1 0 0,0 3,14.5H21A1,1 0 0,0 22,13.5V11.5A1,1 0 0,0 21,10.5M4.5,18.5H19.5V20H4.5V18.5Z" />
        </svg>
        """
    elif icon_type == "involve":
        return """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="#689f38">
            <path d="M12,5.5A3.5,3.5 0 0,1 15.5,9A3.5,3.5 0 0,1 12,12.5A3.5,3.5 0 0,1 8.5,9A3.5,3.5 0 0,1 12,5.5M5,8C5.56,8 6.08,8.15 6.53,8.42C6.38,9.85 6.8,11.27 7.66,12.38C7.16,13.34 6.16,14 5,14A3,3 0 0,1 2,11A3,3 0 0,1 5,8M19,8A3,3 0 0,1 22,11A3,3 0 0,1 19,14C17.84,14 16.84,13.34 16.34,12.38C17.2,11.27 17.62,9.85 17.47,8.42C17.92,8.15 18.44,8 19,8M5.5,18.25C5.5,16.18 8.41,14.5 12,14.5C15.59,14.5 18.5,16.18 18.5,18.25V20H5.5V18.25M0,20V18.5C0,17.11 1.89,15.94 4.45,15.6C3.86,16.28 3.5,17.22 3.5,18.25V20H0M24,20H20.5V18.25C20.5,17.22 20.14,16.28 19.55,15.6C22.11,15.94 24,17.11 24,18.5V20Z" />
        </svg>
        """
    elif icon_type == "education":
        return """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40" fill="#8bc34a">
            <path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z" />
        </svg>
        """
    elif icon_type == "newsletter":
        return """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40" fill="#4caf50">
            <path d="M20,8L12,13L4,8V6L12,11L20,6M20,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V6C22,4.89 21.1,4 20,4Z" />
        </svg>
        """
    elif icon_type == "petition":
        return """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40" fill="#ff9800">
            <path d="M18,22A2,2 0 0,0 20,20V4C20,2.89 19.1,2 18,2H12V9L9.5,7.5L7,9V2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18Z" />
        </svg>
        """
    elif icon_type == "donation":
        return """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40" fill="#66bb6a">
            <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M11,17V16H9V14H13V13H10A1,1 0 0,1 9,12V9A1,1 0 0,1 10,8H11V7H13V8H15V10H11V11H14A1,1 0 0,1 15,12V15A1,1 0 0,1 14,16H13V17H11Z" />
        </svg>
        """
    else:
        return ""

def get_card_impact_stats(card_type):
    """Return impact statistics for cards"""
    if card_type == "reduce":
        return "2.5 tons of CO₂ saved annually by simple individual actions"
    elif card_type == "support":
        return "Over 150M acres protected through conservation partnerships"
    elif card_type == "involve":
        return "20B+ trees planted through global community initiatives"
    return ""

def create_impact_card(icon_svg, title, subtitle, content, impact_stat, theme, card_color, border_color, hover_anim=True):
    """Create a beautiful impact card with animation"""
    is_dark = theme == "dark"
    bg_color = {"reduce": "#063716" if is_dark else "#f1f8e9",
               "support": "#053111" if is_dark else "#e8f5e9", 
               "involve": "#0b3c13" if is_dark else "#dcedc8"}[card_color]
    text_color = "#ffffff" if is_dark else "#2e7d32"
    
    hover_effect = """
    :hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.25);
        transition: all 0.3s ease;
    }
    """ if hover_anim else ""
    
    card_html = f"""
    <div style="
        background-color: {bg_color}; 
        border-radius: 12px; 
        border-left: 5px solid {border_color};
        padding: 20px 25px; 
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        height: 100%;
        {hover_effect}
    ">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="margin-right: 15px;">
                {icon_svg}
            </div>
            <div>
                <h3 style="margin: 0; color: {text_color}; font-size: 20px; font-weight: 600;">{title}</h3>
                <p style="margin: 5px 0 0 0; color: {text_color}; opacity: 0.9; font-size: 15px;">{subtitle}</p>
            </div>
        </div>
        <div style="margin-top: 15px; color: {text_color};">
            {content}
        </div>
        <div style="
            margin-top: 20px;
            background-color: {'rgba(255,255,255,0.1)' if is_dark else 'rgba(46,125,50,0.08)'};
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 14px;
            color: {text_color};
            font-weight: 500;
            display: flex;
            align-items: center;
        ">
            <div style="background-color: {'#4caf50' if is_dark else '#2e7d32'}; 
                      width: 12px; 
                      height: 12px; 
                      border-radius: 50%; 
                      margin-right: 10px;
                      box-shadow: 0 0 8px {'rgba(76,175,80,0.6)' if is_dark else 'rgba(46,125,50,0.4)'};"></div>
            <span>{impact_stat}</span>
        </div>
    </div>
    """
    return card_html

def create_organization_card(org, theme):
    """Create a styled organization card for donations"""
    is_dark = theme == "dark"
    bg_color = "#1a2e1a" if is_dark else "#f8faf8"
    text_color = "#ffffff" if is_dark else "#2e7d32"
    border_color = "#4caf50" if is_dark else "#a5d6a7"
    
    return f"""
    <div style="
        display: flex;
        align-items: center;
        background-color: {bg_color};
        border-radius: 10px;
        border: 1px solid {border_color};
        padding: 16px 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        :hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.12);
        }}
    ">
        <div style="flex: 1;">
            <h4 style="margin: 0 0 5px 0; color: {'#81c784' if is_dark else '#2e7d32'}; font-weight: 600;">{org['name']}</h4>
            <p style="margin: 0; color: {text_color}; font-size: 14px;">{org['description']}</p>
        </div>
        <div>
            <a href="{org['link']}" 
               style="
                  display: inline-block;
                  background-color: {'#1b5e20' if is_dark else '#4caf50'};
                  color: white;
                  padding: 8px 16px;
                  border-radius: 20px;
                  text-decoration: none;
                  font-weight: 500;
                  font-size: 14px;
                  box-shadow: 0 2px 5px rgba(0,0,0,0.15);
                  transition: background-color 0.2s;
                  :hover {{
                      background-color: {'#2e7d32' if is_dark else '#43a047'};
                  }}
               "
               target="_blank">
               Donate Now
            </a>
        </div>
    </div>
    """

def action_section():
    """Display enhanced call-to-action section for conservation efforts."""
    # Create a visually appealing hero section with impact statement
    if st.session_state.theme == "dark":
        hero_bg = "linear-gradient(rgba(7, 31, 15, 0.92), rgba(7, 31, 15, 0.96))"
        hero_text_color = "#ffffff"
        highlight_color = "#81c784"
    else:
        hero_bg = "linear-gradient(rgba(224, 242, 226, 0.8), rgba(232, 245, 233, 0.9))"
        hero_text_color = "#1b5e20"
        highlight_color = "#2e7d32"
    
    st.markdown(f"""
    <div style="
        padding: 40px 30px;
        border-radius: 15px;
        background: {hero_bg};
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    ">
        <h1 style="
            color: {hero_text_color};
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0;
        ">Take Action Now</h1>
        
        <p style="
            color: {hero_text_color};
            font-size: 1.15rem;
            margin: 15px auto 30px auto;
            max-width: 800px;
            line-height: 1.6;
        ">
            Forests are disappearing at a rate of <span style="color: {highlight_color}; font-weight: 600;">26 million acres per year</span>. 
            Your actions today can help protect the lungs of our planet and preserve biodiversity for future generations.
        </p>
        
        <div style="
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
        ">
            <div style="
                background-color: {'rgba(255,255,255,0.15)' if st.session_state.theme == 'dark' else 'rgba(46,125,50,0.08)'};
                border-radius: 50px;
                padding: 12px 20px;
                color: {hero_text_color};
                display: flex;
                align-items: center;
                gap: 10px;
            ">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="{highlight_color}">
                    <path d="M12,2C6.47,2 2,6.47 2,12C2,17.53 6.47,22 12,22C17.53,22 22,17.53 22,12C22,6.47 17.53,2 12,2M15.1,7.07C15.24,7.07 15.38,7.12 15.5,7.23L16.77,8.5C17,8.72 17,9.07 16.77,9.28L15.77,10.28L13.72,8.23L14.72,7.23C14.82,7.12 14.96,7.07 15.1,7.07M13.13,8.81L15.19,10.87L9.13,16.93H7.07V14.87L13.13,8.81Z" />
                </svg>
                <span>3 key ways to contribute</span>
            </div>
            <div style="
                background-color: {'rgba(255,255,255,0.15)' if st.session_state.theme == 'dark' else 'rgba(46,125,50,0.08)'};
                border-radius: 50px;
                padding: 12px 20px;
                color: {hero_text_color};
                display: flex;
                align-items: center;
                gap: 10px;
            ">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="{highlight_color}">
                    <path d="M16.53,11.06L15.47,10L10.59,14.88L8.47,12.76L7.41,13.82L10.59,17L16.53,11.06M12,2C8.14,2 5,5.14 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9C19,5.14 15.86,2 12,2M12,4C14.76,4 17,6.24 17,9C17,11.88 14.12,16.19 12,18.88C9.92,16.21 7,11.85 7,9C7,6.24 9.24,4 12,4Z" />
                </svg>
                <span>Track impact globally</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for different action categories with enhanced styling
    st.markdown("<h2 style='margin-bottom: 25px; font-weight: 600;'>Ways You Can Make a Difference</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Reduce Your Impact card
    with col1:
        reduce_icon = create_svg_icon("reduce")
        reduce_content = """
        <ul style="padding-left: 20px; margin-top: 0;">
            <li style="margin-bottom: 8px;">Choose recycled or FSC-certified paper products</li>
            <li style="margin-bottom: 8px;">Reduce meat consumption, especially beef</li>
            <li style="margin-bottom: 8px;">Use digital documents instead of printing</li>
            <li style="margin-bottom: 8px;">Support sustainable palm oil products</li>
            <li>Buy furniture from sustainable sources</li>
        </ul>
        """
        reduce_stats = get_card_impact_stats("reduce")
        reduce_card = create_impact_card(
            reduce_icon, 
            "Reduce Your Impact", 
            "Simple daily actions to help forests",
            reduce_content,
            reduce_stats,
            st.session_state.theme,
            "reduce",
            "#43a047"
        )
        st.markdown(reduce_card, unsafe_allow_html=True)
    
    # Support Organizations card
    with col2:
        support_icon = create_svg_icon("support")
        support_content = """
        <ul style="padding-left: 20px; margin-top: 0;">
            <li style="margin-bottom: 8px;"><a href="https://www.rainforest-alliance.org/" target="_blank" style="color: inherit;">Rainforest Alliance</a></li>
            <li style="margin-bottom: 8px;"><a href="https://www.worldwildlife.org/" target="_blank" style="color: inherit;">World Wildlife Fund</a></li>
            <li style="margin-bottom: 8px;"><a href="https://www.conservation.org/" target="_blank" style="color: inherit;">Conservation International</a></li>
            <li style="margin-bottom: 8px;"><a href="https://www.nature.org/" target="_blank" style="color: inherit;">The Nature Conservancy</a></li>
            <li><a href="https://www.amazonteam.org/" target="_blank" style="color: inherit;">Amazon Conservation Team</a></li>
        </ul>
        """
        support_stats = get_card_impact_stats("support")
        support_card = create_impact_card(
            support_icon, 
            "Support Organizations", 
            "Conservation groups fighting deforestation",
            support_content,
            support_stats,
            st.session_state.theme,
            "support",
            "#2e7d32"
        )
        st.markdown(support_card, unsafe_allow_html=True)
    
    # Get Involved card
    with col3:
        involve_icon = create_svg_icon("involve")
        involve_content = """
        <ul style="padding-left: 20px; margin-top: 0;">
            <li style="margin-bottom: 8px;">Participate in local tree planting events</li>
            <li style="margin-bottom: 8px;">Volunteer with conservation organizations</li>
            <li style="margin-bottom: 8px;">Support political actions for forest protection</li>
            <li style="margin-bottom: 8px;">Start a community garden</li>
            <li>Educate others about deforestation</li>
        </ul>
        """
        involve_stats = get_card_impact_stats("involve")
        involve_card = create_impact_card(
            involve_icon, 
            "Get Involved", 
            "Direct action opportunities",
            involve_content,
            involve_stats,
            st.session_state.theme,
            "involve",
            "#689f38"
        )
        st.markdown(involve_card, unsafe_allow_html=True)
    
    # Create tabbed sections for further actions
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)  # Spacing
    
    tabs = st.tabs(["📚 Educational Resources", "📧 Stay Updated", "✍️ Sign Petition", "💰 Donate"])
    
    # Tab 1: Educational Resources
    with tabs[0]:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(create_svg_icon("education"), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            ## Expand Your Knowledge
            
            Education is a powerful tool in the fight against deforestation. The more people understand about the importance of forests and the threats they face, the more likely they are to take action.
            """)
        
        # Create three columns for different resource types
        docs_col, books_col, courses_col = st.columns(3)
        
        with docs_col:
            st.markdown("""
            ### 🎬 Documentaries
            
            - **"Our Planet"** (Netflix)  
              *Explores the Earth's natural wonders and the impact of humans*
              
            - **"A Life on Our Planet"** (Netflix)  
              *David Attenborough's witness statement for the natural world*
              
            - **"The Amazon"** (National Geographic)  
              *In-depth exploration of the Amazon rainforest*
              
            - **"Chasing Coral"** (Netflix)  
              *Shows the impact of climate change on coral reefs*
            """)
            
        with books_col:
            st.markdown("""
            ### 📖 Books
            
            - **"The World's Forests"**  
              *by James Barlow - Comprehensive overview of global forests*
              
            - **"The Hidden Life of Trees"**  
              *by Peter Wohlleben - Reveals the complex life of trees*
              
            - **"The Sixth Extinction"**  
              *by Elizabeth Kolbert - Pulitzer Prize winner on extinction*
              
            - **"Drawdown"**  
              *by Paul Hawken - Practical solutions to climate change*
            """)
            
        with courses_col:
            st.markdown("""
            ### 🖥️ Online Courses
            
            - **[Conservation and Protected Area Management](https://www.edx.org/course/conservation-protected-area-management-course-v1queensu-environmental-managementx)**  
              *Learn conservation strategies and practices*
              
            - **[Tropical Forest Landscapes](https://www.edx.org/course/tropical-forest-landscapes)**  
              *Understand tropical forest ecology and management*
              
            - **[Introduction to Sustainability](https://www.coursera.org/learn/sustainability)**  
              *Broad overview of sustainability concepts*
            """)
    
    # Tab 2: Newsletter Signup
    with tabs[1]:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(create_svg_icon("newsletter"), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            ## Stay Updated
            
            Receive the latest news, research findings, and action alerts about deforestation and conservation efforts worldwide. Our newsletter provides curated content to keep you informed and engaged.
            """)
        
        # Create a more professional newsletter form
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Spacing
        
        with st.form("newsletter_form_enhanced"):
            form_col1, form_col2 = st.columns([3, 2])
            
            with form_col1:
                st.markdown("##### Your Information")
                name = st.text_input("Full Name", placeholder="Jane Doe", key="newsletter_name")
                email = st.text_input("Email Address", placeholder="your.email@example.com", key="newsletter_email")
            
            with form_col2:
                st.markdown("##### Areas of Interest")
                st.markdown("<div style='height: 9px;'></div>", unsafe_allow_html=True)  # Alignment spacing
                interests = st.multiselect(
                    "Select topics you're interested in",
                    options=["Amazon Rainforest", "Borneo", "Congo Basin", "Other Regions", "Conservation Projects", "Policy Updates", "Community Initiatives", "Scientific Research"],
                    key="newsletter_interests"
                )
            
            frequency = st.radio(
                "Newsletter Frequency",
                options=["Weekly Digest", "Monthly Summary", "Major Updates Only"],
                horizontal=True,
                key="newsletter_frequency"
            )
            
            privacy_agree = st.checkbox("I agree to receive emails and understand I can unsubscribe at any time", key="newsletter_privacy")
            
            submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
            
            with submit_col2:
                submit = st.form_submit_button("Subscribe to Newsletter", use_container_width=True)
            
            if submit:
                if email and "@" in email and "." in email and privacy_agree:
                    st.success(f"Thank you, {name if name else 'Friend'}! You've been subscribed to our {frequency.lower()}.")
                    st.markdown("""
                    <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 15px;">
                        <p style="margin: 0; color: #2e7d32;">
                            <strong>What's next:</strong> Check your inbox for a confirmation email. 
                            We've sent you a welcome guide with our latest conservation report.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if not email or "@" not in email or "." not in email:
                        st.error("Please enter a valid email address.")
                    if not privacy_agree:
                        st.error("Please agree to the privacy terms to continue.")
    
    # Tab 3: Petition
    with tabs[2]:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(create_svg_icon("petition"), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            ## Sign Our Petition
            
            Join thousands of others in calling for stronger protections for the world's forests. 
            Your voice can make a difference in shaping conservation policies.
            """)
            
        # Create a more visually appealing petition section
        petition_count = 8742  # Simulated number of signatures
        goal = 10000
        progress_percent = petition_count / goal
        
        st.markdown(f"""
        <div style="
            background: {'#1a2e1a' if st.session_state.theme == 'dark' else '#f1f8e9'}; 
            border-radius: 12px; 
            padding: 20px; 
            margin: 20px 0; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-weight: 600; font-size: 16px; color: {'#ffffff' if st.session_state.theme == 'dark' else '#2e7d32'};">
                    Petition Progress
                </div>
                <div style="font-weight: 600; font-size: 16px; color: {'#81c784' if st.session_state.theme == 'dark' else '#2e7d32'};">
                    {petition_count:,} / {goal:,} signatures
                </div>
            </div>
            <div style="
                width: 100%; 
                height: 12px; 
                background-color: {'rgba(255,255,255,0.1)' if st.session_state.theme == 'dark' else 'rgba(46,125,50,0.1)'};
                border-radius: 6px;
                overflow: hidden;
            ">
                <div style="
                    width: {progress_percent * 100}%; 
                    height: 100%; 
                    background: linear-gradient(90deg, {'#388e3c' if st.session_state.theme == 'dark' else '#4caf50'}, {'#66bb6a' if st.session_state.theme == 'dark' else '#66bb6a'});
                    border-radius: 6px;
                "></div>
            </div>
            <div style="margin-top: 10px; font-size: 14px; color: {'#ffffff' if st.session_state.theme == 'dark' else '#2e7d32'}; opacity: 0.8;">
                We need {goal - petition_count:,} more signatures to reach our goal
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("petition_form_enhanced"):
            st.markdown("### Add Your Voice")
            
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Full Name", key="petition_name")
                email = st.text_input("Email Address", key="petition_email")
            
            with cols[1]:
                country = st.selectbox(
                    "Country",
                    options=["United States", "Canada", "United Kingdom", "Australia", "Germany", "France", "Brazil", "India", "China", "Japan", "Mexico", "South Africa", "Other"],
                    key="petition_country"
                )
                age_group = st.selectbox(
                    "Age Group",
                    options=["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+", "Prefer not to say"],
                    key="petition_age"
                )
            
            reason = st.text_area(
                "Why is forest conservation important to you? (Optional)",
                max_chars=200,
                height=100,
                key="petition_reason"
            )
            
            checkboxes = st.columns(2)
            with checkboxes[0]:
                agree_display = st.checkbox("I agree to have my name displayed publicly as a supporter", key="petition_agree_display")
            
            with checkboxes[1]:
                agree_updates = st.checkbox("I would like to receive updates about this petition", key="petition_agree_updates")
            
            submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
            with submit_col2:
                submit_petition = st.form_submit_button("Sign the Petition", use_container_width=True)
            
            if submit_petition:
                if name and email and agree_display:
                    st.success(f"Thank you, {name}! Your signature has been added to our petition.")
                    st.balloons()
                    
                    st.markdown(f"""
                    <div style="background-color: {'#1c3b1c' if st.session_state.theme == 'dark' else '#e8f5e9'}; padding: 15px; border-radius: 10px; margin-top: 15px;">
                        <p style="margin: 0; color: {'#ffffff' if st.session_state.theme == 'dark' else '#2e7d32'};">
                            <strong>Share this petition:</strong> Help us reach our goal by sharing this petition with your network.
                            The more signatures we collect, the stronger our voice will be!
                        </p>
                        <div style="display: flex; gap: 10px; margin-top: 10px;">
                            <a href="#" style="
                                background-color: #3b5998; 
                                color: white; 
                                padding: 8px 16px; 
                                border-radius: 4px; 
                                text-decoration: none; 
                                font-weight: 500;
                                font-size: 14px;">
                                Share on Facebook
                            </a>
                            <a href="#" style="
                                background-color: #1da1f2; 
                                color: white; 
                                padding: 8px 16px; 
                                border-radius: 4px; 
                                text-decoration: none; 
                                font-weight: 500;
                                font-size: 14px;">
                                Share on Twitter
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if not name:
                        st.error("Please enter your name.")
                    if not email:
                        st.error("Please enter your email address.")
                    if not agree_display:
                        st.error("You must agree to have your name displayed publicly.")
    
    # Tab 4: Donation
    with tabs[3]:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(create_svg_icon("donation"), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            ## Support Conservation Efforts
            
            Your financial contribution can directly support forest conservation projects around the world.
            Even small donations can have a significant impact when directed to effective organizations.
            """)
        
        # Create an impact counter section
        st.markdown("""
        <div style="
            display: flex;
            justify-content: space-between;
            text-align: center;
            margin: 30px 0;
        ">
            <div style="flex: 1;">
                <div style="
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: #4caf50;
                    margin-bottom: 5px;
                ">$25</div>
                <div style="font-size: 0.9rem;">Plants 25 trees</div>
            </div>
            <div style="flex: 1;">
                <div style="
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: #4caf50;
                    margin-bottom: 5px;
                ">$100</div>
                <div style="font-size: 0.9rem;">Protects 1 acre of forest</div>
            </div>
            <div style="flex: 1;">
                <div style="
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: #4caf50;
                    margin-bottom: 5px;
                ">$500</div>
                <div style="font-size: 0.9rem;">Funds monitoring equipment</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced organization cards
        st.markdown("### Trusted Conservation Organizations")
        
        orgs = [
            {
                "name": "Rainforest Trust",
                "description": "Purchases and protects the most threatened tropical forests, saving endangered wildlife through partnerships.",
                "link": "https://www.rainforesttrust.org/",
                "impact": "Has protected over 37 million acres of rainforest"
            },
            {
                "name": "One Tree Planted",
                "description": "Plants one tree for every dollar donated in various regions around the world with a focus on sustainability.",
                "link": "https://onetreeplanted.org/",
                "impact": "Planted over 40 million trees across 47 countries"
            },
            {
                "name": "Amazon Watch",
                "description": "Protects the rainforest and advances indigenous rights in the Amazon Basin through advocacy and partnerships.",
                "link": "https://amazonwatch.org/",
                "impact": "Successfully protected over 5 million acres of indigenous lands"
            },
            {
                "name": "Rainforest Foundation",
                "description": "Supports indigenous peoples and traditional populations in their efforts to protect their environment and fulfill their rights.",
                "link": "https://rainforestfoundation.org/",
                "impact": "Secured legal protection for over 33 million acres of forest"
            }
        ]
        
        for org in orgs:
            st.markdown(create_organization_card(org, st.session_state.theme), unsafe_allow_html=True)
            
        # Add a special featured project
        is_dark = st.session_state.theme == "dark"
        
        st.markdown("""
        <div style="height: 30px;"></div>
        <h3>Featured Conservation Project</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.7)), url('https://i.imgur.com/g6BK5TH.jpg');
            background-size: cover;
            background-position: center;
            padding: 40px 30px;
            border-radius: 15px;
            color: white;
            margin: 10px 0 30px 0;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        ">
            <h2 style="margin-top: 0;">Borneo Orangutan Habitat Protection</h2>
            <p style="font-size: 1.1rem; max-width: 80%; margin-bottom: 20px;">
                A critical initiative to protect 50,000 acres of orangutan habitat in Borneo from palm oil expansion.
                This project will create wildlife corridors connecting fragmented forest areas.
            </p>
            <div style="
                background-color: rgba(255,255,255,0.1);
                padding: 12px 20px;
                border-radius: 8px;
                display: inline-block;
                margin-bottom: 20px;
            ">
                <span style="font-weight: 600;">65% Funded</span> • <span>$325,000 of $500,000 goal</span>
            </div>
            <br>
            <a href="#" style="
                display: inline-block;
                background-color: #4caf50;
                color: white;
                padding: 12px 24px;
                border-radius: 30px;
                text-decoration: none;
                font-weight: 600;
                font-size: 16px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            ">Support This Project</a>
        </div>
        """, unsafe_allow_html=True)