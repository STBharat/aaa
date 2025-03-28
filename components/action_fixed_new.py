import streamlit as st
from streamlit_extras.colored_header import colored_header

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
    
    # Create a fixed hero section
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
    
    # Create action cards with simplified styling
    st.markdown("## Ways You Can Make a Difference")
    
    # Create three columns for the impact cards
    col1, col2, col3 = st.columns(3)
    
    # Reduce Your Impact card
    with col1:
        st.markdown("""
        <div style="
            background-color: #f1f8e9; 
            border-radius: 12px; 
            border-left: 5px solid #43a047;
            padding: 20px 25px; 
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            height: 100%;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="margin-right: 15px;">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="#4caf50">
                        <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,10.5A1.5,1.5 0 0,1 13.5,12A1.5,1.5 0 0,1 12,13.5A1.5,1.5 0 0,1 10.5,12A1.5,1.5 0 0,1 12,10.5M7.5,12A1.5,1.5 0 0,1 9,13.5A1.5,1.5 0 0,1 7.5,15A1.5,1.5 0 0,1 6,13.5A1.5,1.5 0 0,1 7.5,12M16.5,12A1.5,1.5 0 0,1 18,13.5A1.5,1.5 0 0,1 16.5,15A1.5,1.5 0 0,1 15,13.5A1.5,1.5 0 0,1 16.5,12Z" />
                    </svg>
                </div>
                <div>
                    <h3 style="margin: 0; color: #2e7d32; font-size: 20px; font-weight: 600;">Reduce Your Impact</h3>
                    <p style="margin: 5px 0 0 0; color: #2e7d32; opacity: 0.9; font-size: 15px;">Simple daily actions to help forests</p>
                </div>
            </div>
            <div style="margin-top: 15px; color: #2e7d32;">
                <ul style="padding-left: 20px; margin-top: 0;">
                    <li style="margin-bottom: 8px;">Choose recycled or FSC-certified paper products</li>
                    <li style="margin-bottom: 8px;">Reduce meat consumption, especially beef</li>
                    <li style="margin-bottom: 8px;">Use digital documents instead of printing</li>
                    <li style="margin-bottom: 8px;">Support sustainable palm oil products</li>
                    <li>Buy furniture from sustainable sources</li>
                </ul>
            </div>
            <div style="
                margin-top: 20px;
                background-color: rgba(46,125,50,0.08);
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                color: #2e7d32;
                font-weight: 500;
                display: flex;
                align-items: center;
            ">
                <div style="background-color: #2e7d32; 
                          width: 12px; 
                          height: 12px; 
                          border-radius: 50%; 
                          margin-right: 10px;
                          box-shadow: 0 0 8px rgba(46,125,50,0.4);"></div>
                <span>2.5 tons of CO₂ saved annually by simple individual actions</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Support Organizations card
    with col2:
        st.markdown("""
        <div style="
            background-color: #e8f5e9; 
            border-radius: 12px; 
            border-left: 5px solid #2e7d32;
            padding: 20px 25px; 
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            height: 100%;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="margin-right: 15px;">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="#2e7d32">
                        <path d="M21,10.5H20V8H17V10.5H16.5V7H14V10.5H13.5V5H11V10.5H10.5V8H7.5V10.5H7V7H4V10.5H3A1,1 0 0,0 2,11.5V13.5A1,1 0 0,0 3,14.5H21A1,1 0 0,0 22,13.5V11.5A1,1 0 0,0 21,10.5M4.5,18.5H19.5V20H4.5V18.5Z" />
                    </svg>
                </div>
                <div>
                    <h3 style="margin: 0; color: #2e7d32; font-size: 20px; font-weight: 600;">Support Organizations</h3>
                    <p style="margin: 5px 0 0 0; color: #2e7d32; opacity: 0.9; font-size: 15px;">Conservation groups fighting deforestation</p>
                </div>
            </div>
            <div style="margin-top: 15px; color: #2e7d32;">
                <ul style="padding-left: 20px; margin-top: 0;">
                    <li style="margin-bottom: 8px;"><a href="https://www.rainforest-alliance.org/" target="_blank" style="color: inherit;">Rainforest Alliance</a></li>
                    <li style="margin-bottom: 8px;"><a href="https://www.worldwildlife.org/" target="_blank" style="color: inherit;">World Wildlife Fund</a></li>
                    <li style="margin-bottom: 8px;"><a href="https://www.conservation.org/" target="_blank" style="color: inherit;">Conservation International</a></li>
                    <li style="margin-bottom: 8px;"><a href="https://www.nature.org/" target="_blank" style="color: inherit;">The Nature Conservancy</a></li>
                    <li><a href="https://www.amazonteam.org/" target="_blank" style="color: inherit;">Amazon Conservation Team</a></li>
                </ul>
            </div>
            <div style="
                margin-top: 20px;
                background-color: rgba(46,125,50,0.08);
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                color: #2e7d32;
                font-weight: 500;
                display: flex;
                align-items: center;
            ">
                <div style="background-color: #2e7d32; 
                          width: 12px; 
                          height: 12px; 
                          border-radius: 50%; 
                          margin-right: 10px;
                          box-shadow: 0 0 8px rgba(46,125,50,0.4);"></div>
                <span>Over 150M acres protected through conservation partnerships</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Get Involved card
    with col3:
        st.markdown("""
        <div style="
            background-color: #dcedc8; 
            border-radius: 12px; 
            border-left: 5px solid #33691e;
            padding: 20px 25px; 
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            height: 100%;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="margin-right: 15px;">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="#689f38">
                        <path d="M12,5.5A3.5,3.5 0 0,1 15.5,9A3.5,3.5 0 0,1 12,12.5A3.5,3.5 0 0,1 8.5,9A3.5,3.5 0 0,1 12,5.5M5,8C5.56,8 6.08,8.15 6.53,8.42C6.38,9.85 6.8,11.27 7.66,12.38C7.16,13.34 6.16,14 5,14A3,3 0 0,1 2,11A3,3 0 0,1 5,8M19,8A3,3 0 0,1 22,11A3,3 0 0,1 19,14C17.84,14 16.84,13.34 16.34,12.38C17.2,11.27 17.62,9.85 17.47,8.42C17.92,8.15 18.44,8 19,8M5.5,18.25C5.5,16.18 8.41,14.5 12,14.5C15.59,14.5 18.5,16.18 18.5,18.25V20H5.5V18.25M0,20V18.5C0,17.11 1.89,15.94 4.45,15.6C3.86,16.28 3.5,17.22 3.5,18.25V20H0M24,20H20.5V18.25C20.5,17.22 20.14,16.28 19.55,15.6C22.11,15.94 24,17.11 24,18.5V20Z" />
                    </svg>
                </div>
                <div>
                    <h3 style="margin: 0; color: #2e7d32; font-size: 20px; font-weight: 600;">Get Involved</h3>
                    <p style="margin: 5px 0 0 0; color: #2e7d32; opacity: 0.9; font-size: 15px;">Direct action opportunities</p>
                </div>
            </div>
            <div style="margin-top: 15px; color: #2e7d32;">
                <ul style="padding-left: 20px; margin-top: 0;">
                    <li style="margin-bottom: 8px;">Participate in local tree planting events</li>
                    <li style="margin-bottom: 8px;">Volunteer with conservation organizations</li>
                    <li style="margin-bottom: 8px;">Support political actions for forest protection</li>
                    <li style="margin-bottom: 8px;">Start a community garden</li>
                    <li>Educate others about deforestation</li>
                </ul>
            </div>
            <div style="
                margin-top: 20px;
                background-color: rgba(46,125,50,0.08);
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                color: #2e7d32;
                font-weight: 500;
                display: flex;
                align-items: center;
            ">
                <div style="background-color: #2e7d32; 
                          width: 12px; 
                          height: 12px; 
                          border-radius: 50%; 
                          margin-right: 10px;
                          box-shadow: 0 0 8px rgba(46,125,50,0.4);"></div>
                <span>20B+ trees planted through global community initiatives</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create a tabbed section below for more specific actions
    st.markdown("## Get Started Now")
    tabs = st.tabs(["📚 Educational Resources", "📧 Stay Updated", "✍️ Sign Petition", "💰 Donate"])
    
    # Tab 1: Educational Resources
    with tabs[0]:
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
        st.markdown("""
        ## Add Your Voice
        
        Sign petitions to support legislation that protects forests and holds companies accountable for sustainable practices. Your signature matters!
        """)
        
        # Create a petition sign-up section
        st.markdown("### Sign Our Petition")
        
        with st.form("petition_form"):
            st.markdown("""
            **We call on world leaders to:**
            1. Enact stronger deforestation protection laws
            2. Hold corporations accountable for supply chain sustainability
            3. Support indigenous land rights and forest protection
            4. Increase funding for forest conservation and restoration
            5. Create economic incentives for sustainable practices
            """)
            
            cols = st.columns([1, 1, 1])
            with cols[0]:
                name = st.text_input("Full Name", key="petition_name")
            with cols[1]:
                email = st.text_input("Email Address", key="petition_email")
            with cols[2]:
                country = st.selectbox("Country", 
                                     ["United States", "Canada", "United Kingdom", "Australia", 
                                      "Germany", "France", "Brazil", "India", "Japan", "Other"])
            
            reason = st.text_area("Why is this important to you? (Optional)", height=80)
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.checkbox("I agree to share my information with relevant decision-makers", value=True)
            with col2:
                submit = st.form_submit_button("Sign Petition")
                
            if submit:
                if not name or not email:
                    st.error("Please enter your name and email to sign the petition.")
                else:
                    st.success(f"Thank you for signing, {name.split()[0]}! Your voice makes a difference.")
                    st.markdown(f"**Signatures so far:** 24,731")
        
        # Show other related petitions
        st.markdown("### Other Important Petitions")
        
        petitions = [
            {"title": "Stop Amazon Deforestation", "org": "Rainforest Action Network", "signatures": "348,912", "url": "#"},
            {"title": "Protect Sumatran Tiger Habitat", "org": "WWF", "signatures": "156,237", "url": "#"},
            {"title": "Ban Single-Use Plastics in Forests", "org": "Earth First", "signatures": "89,452", "url": "#"}
        ]
        
        for petition in petitions:
            st.markdown(f"""
            <div style="
                padding: 15px; 
                border-radius: 8px; 
                background-color: rgba(76, 175, 80, 0.05);
                margin-bottom: 10px;
                border-left: 3px solid #4CAF50;
            ">
                <div style="font-weight: 600; color: #2e7d32;">{petition['title']}</div>
                <div style="font-size: 0.9rem; margin: 5px 0;">{petition['org']} · {petition['signatures']} signatures</div>
                <a href="{petition['url']}" target="_blank" style="
                    display: inline-block;
                    font-size: 0.9rem;
                    color: #2e7d32;
                    text-decoration: none;
                    font-weight: 500;
                ">Sign this petition →</a>
            </div>
            """, unsafe_allow_html=True)
            
    # Tab 4: Donate
    with tabs[3]:
        st.markdown("""
        ## Support Conservation Financially
        
        Your donations can make a significant impact in protecting forests worldwide. Even small contributions add up to make a big difference.
        """)
        
        # Create a highlight section showing impact of donations
        st.markdown("""
        <div style="
            background-color: rgba(76, 175, 80, 0.1);
            border-radius: 12px;
            padding: 20px 25px;
            margin: 20px 0;
        ">
            <h3 style="margin-top: 0; color: #2e7d32; font-size: 20px;">Impact of Your Donation</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 28px; font-weight: 600; color: #2e7d32;">$25</div>
                    <div style="color: #2e7d32;">Plants 25 trees in deforested areas</div>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 28px; font-weight: 600; color: #2e7d32;">$50</div>
                    <div style="color: #2e7d32;">Protects 1 acre of rainforest for a year</div>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 28px; font-weight: 600; color: #2e7d32;">$100</div>
                    <div style="color: #2e7d32;">Funds 1 day of anti-poaching patrol</div>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 28px; font-weight: 600; color: #2e7d32;">$500</div>
                    <div style="color: #2e7d32;">Supports local community conservation for a month</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a list of featured organizations
        st.markdown("### Featured Organizations")
        
        organizations = [
            "Rainforest Alliance", 
            "World Wildlife Fund", 
            "Conservation International",
            "The Nature Conservancy", 
            "Amazon Conservation Team"
        ]
        
        for org in organizations:
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                background-color: #f8faf8;
                border-radius: 10px;
                border: 1px solid #a5d6a7;
                padding: 16px 20px;
                margin-bottom: 15px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.08);
            ">
                <div style="flex: 1;">
                    <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 5px; color: #2e7d32;">
                        {org}
                    </div>
                </div>
                <div>
                    <a href="#" style="
                        display: inline-block;
                        text-decoration: none;
                        padding: 8px 16px;
                        background-color: #e8f5e9;
                        color: #2e7d32;
                        border-radius: 20px;
                        font-size: 0.9rem;
                        font-weight: 500;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    ">Visit Website</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a direct donation option
        st.markdown("### Make a Direct Donation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.selectbox("Select Amount", 
                                ["$25", "$50", "$100", "$250", "$500", "Other"])
            if amount == "Other":
                custom_amount = st.number_input("Enter Amount ($)", min_value=1, value=75)
        
        with col2:
            frequency = st.radio("Donation Frequency", 
                                ["One-time", "Monthly", "Quarterly", "Annually"])
            
        # Donation button
        if st.button("Donate Now", type="primary"):
            final_amount = custom_amount if amount == "Other" else amount
            st.success(f"Thank you for your {frequency.lower()} donation of {final_amount}! Redirecting to secure payment...")
            
        st.markdown("""
        <div style="font-size: 0.8rem; color: #666666; margin-top: 10px;">
        All donations are tax-deductible. You'll receive a receipt for your records.
        </div>
        """, unsafe_allow_html=True)