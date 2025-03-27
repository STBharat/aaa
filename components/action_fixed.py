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
    
    # Using CSS classname styling
    card_html = f"""
    <div style="
        background-color: {bg_color}; 
        border-radius: 12px; 
        border-left: 5px solid {border_color};
        padding: 20px 25px; 
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        height: 100%;
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
    ">
        <div style="flex: 1;">
            <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 5px; color: {text_color};">
                {org["name"]}
            </div>
            <div style="font-size: 0.9rem; margin-bottom: 8px; color: {text_color}; opacity: 0.9;">
                {org["description"]}
            </div>
            <div style="font-size: 0.8rem; color: {'#81c784' if is_dark else '#2e7d32'}; font-weight: 500;">
                {org["impact"]}
            </div>
        </div>
        <div>
            <a href="{org["link"]}" target="_blank" style="
                display: inline-block;
                text-decoration: none;
                padding: 8px 16px;
                background-color: {'#2e7d32' if is_dark else '#e8f5e9'};
                color: {'#ffffff' if is_dark else '#2e7d32'};
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: 500;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: all 0.2s ease;
            ">Visit Website</a>
        </div>
    </div>
    """

def action_section():
    """Display enhanced call-to-action section for conservation efforts."""
    # Create a session state to track tab changes if not already created
    if 'action_tab' not in st.session_state:
        st.session_state.action_tab = 0
        
    # Create a header with green styling for the page
    colored_header(
        label="Take Action for Forest Conservation",
        description="Join the effort to stop deforestation and restore forests globally",
        color_name="green-70",
    )
    
    # Create a fixed hero section that doesn't rely on CSS classes or hover effects
    st.markdown("""
    <div style="
        color: #1b5e20;
        font-size: 1.15rem;
        margin: 15px auto 30px auto;
        max-width: 800px;
        line-height: 1.6;
        text-align: center;
    ">
        Forests are disappearing at a rate of <span style="color: #2e7d32; font-weight: 600;">26 million acres per year</span>. 
        Your actions today can help protect the lungs of our planet and preserve biodiversity for future generations.
    </div>
    
    <div style="
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 15px auto 30px auto;
        max-width: 800px;
    ">
        <div style="
            background-color: rgba(46,125,50,0.08);
            border-radius: 50px;
            padding: 12px 20px;
            color: #1b5e20;
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#2e7d32">
                <path d="M12,2C6.47,2 2,6.47 2,12C2,17.53 6.47,22 12,22C17.53,22 22,17.53 22,12C22,6.47 17.53,2 12,2M15.1,7.07C15.24,7.07 15.38,7.12 15.5,7.23L16.77,8.5C17,8.72 17,9.07 16.77,9.28L15.77,10.28L13.72,8.23L14.72,7.23C14.82,7.12 14.96,7.07 15.1,7.07M13.13,8.81L15.19,10.87L9.13,16.93H7.07V14.87L13.13,8.81Z" />
            </svg>
            <span>3 key ways to contribute</span>
        </div>
        <div style="
            background-color: rgba(46,125,50,0.08);
            border-radius: 50px;
            padding: 12px 20px;
            color: #1b5e20;
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#2e7d32">
                <path d="M16.53,11.06L15.47,10L10.59,14.88L8.47,12.76L7.41,13.82L10.59,17L16.53,11.06M12,2C8.14,2 5,5.14 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9C19,5.14 15.86,2 12,2M12,4C14.76,4 17,6.24 17,9C17,11.88 14.12,16.19 12,18.88C9.92,16.21 7,11.85 7,9C7,6.24 9.24,4 12,4Z" />
            </svg>
            <span>Track impact globally</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create action cards without hover effects
    st.markdown("## Ways You Can Make a Difference")
    
    # Create three columns for the impact cards
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
            "#43a047",
            hover_anim=False
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
            "#2e7d32",
            hover_anim=False
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
            "#33691e",
            hover_anim=False
        )
        st.markdown(involve_card, unsafe_allow_html=True)
    
    # Create a tabbed section below for more specific actions
    st.markdown("## Get Started Now")
    tabs = st.tabs(["📚 Educational Resources", "📧 Stay Updated", "✍️ Sign Petition", "💰 Donate"])
    
    # Tab 1: Educational Resources
    with tabs[0]:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(create_svg_icon("education"), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            ## Learn and Share
            
            Education is a powerful tool in the fight against deforestation. The more people understand about the importance of forests and the threats they face, the more likely they are to take action.
            """)
            
        st.markdown("### Key Resources")
        
        # Create two columns for resources
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown("""
            #### Articles & Research
            * [The State of the World's Forests (FAO)](https://www.fao.org/state-of-forests/en/)
            * [Causes of Deforestation (Greenpeace)](https://www.greenpeace.org/international/tag/forests/)
            * [Impacts of Deforestation on Climate (NASA)](https://climate.nasa.gov/news/2927/examining-the-viability-of-planting-trees-to-help-mitigate-climate-change/)
            * [Role of Indigenous Communities in Forest Conservation](https://www.worldwildlife.org/magazine/issues/fall-2018/articles/indigenous-peoples-and-conservation)
            """)
            
        with res_col2:
            st.markdown("""
            #### Documentaries & Media
            * "Our Planet" - Netflix series
            * "Chasing Coral" - Documentary
            * "A Life on Our Planet" - David Attenborough
            * "The Serengeti Rules" - PBS Documentary
            * "The Red Forest" - Short Film
            """)
            
        # Add a section for educational tools for different audiences
        st.markdown("### Educational Tools")
        
        edu_col1, edu_col2, edu_col3 = st.columns(3)
        
        with edu_col1:
            st.markdown("""
            #### For Teachers
            * Classroom lesson plans
            * Field trip guides
            * Interactive activities
            * Virtual forest tours
            """)
            
        with edu_col2:
            st.markdown("""
            #### For Students
            * Research project ideas
            * Virtual labs
            * Science fair projects
            * Career exploration
            """)
            
        with edu_col3:
            st.markdown("""
            #### For Communities
            * Workshop materials
            * Community project guides
            * Local forest information
            * Group discussion kits
            """)
            
    # Tab 2: Stay Updated
    with tabs[1]:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(create_svg_icon("newsletter"), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            ## Stay Informed
            
            Receive regular updates on deforestation trends, conservation wins, and opportunities to get involved. Our newsletter focuses on actionable information and positive developments.
            """)
        
        # Create a newsletter sign-up section
        st.markdown("### Join Our Newsletter")
        
        with st.form("newsletter_form"):
            cols = st.columns([2, 2, 1])
            with cols[0]:
                name = st.text_input("Your Name")
            with cols[1]:
                email = st.text_input("Email Address")
            with cols[2]:
                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Subscribe")
                
            if submit:
                if not email:
                    st.error("Please enter your email address.")
                else:
                    st.success(f"Thank you for subscribing, {name if name else 'Friend'}! You'll receive our next update soon.")
            
        st.markdown("""
        ### What You'll Receive
        
        * Monthly newsletter with conservation updates
        * Breaking news alerts on critical forest issues
        * Seasonal reports on deforestation trends
        * Invitations to webinars and virtual events
        * Opportunities to participate in conservation projects
        """)
        
        # Add preference toggles
        st.markdown("### Content Preferences")
        st.caption("Tell us what you're most interested in receiving:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Scientific research updates", value=True)
            st.checkbox("Policy and legislation news", value=True)
            st.checkbox("Conservation success stories", value=True)
        
        with col2:
            st.checkbox("Volunteer opportunities", value=True)
            st.checkbox("Educational resources", value=True)
            st.checkbox("Funding and donation needs", value=False)
        
    # Tab 3: Sign Petition
    with tabs[2]:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(create_svg_icon("petition"), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            ## Add Your Voice
            
            Petitions can be powerful tools for policy change. When thousands of voices unite around a shared cause, decision-makers take notice. Sign our petition to strengthen forest protection laws.
            """)
        
        st.markdown("""
        ### Current Petition: Strengthen International Deforestation Laws
        
        We are calling on the United Nations Environment Programme to establish stronger international protections for primary forests, with enforceable consequences for non-compliance.
        
        **Current signatures:** 12,487 • **Goal:** 25,000
        """)
        
        # Progress bar for petition
        st.progress(12487/25000)
        
        # Create a form for the petition
        with st.form("petition_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                
            with col2:
                country = st.selectbox("Country", 
                                    ["Select Country", "United States", "Canada", "United Kingdom", 
                                     "Australia", "Germany", "France", "Brazil", "Indonesia", 
                                     "India", "China", "Other"])
                reason = st.text_area("Why are you signing? (Optional)", height=100)
            
            # Add a checkbox for agreements
            agree_display = st.checkbox("I agree to have my name displayed publicly with this petition")
            agree_updates = st.checkbox("I would like to receive updates about this campaign", value=True)
            
            # Submit button
            submitted = st.form_submit_button("Sign Petition")
            
            if submitted:
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