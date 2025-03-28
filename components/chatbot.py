import streamlit as st
from streamlit_extras.colored_header import colored_header
from PIL import Image
import base64
import io

def chatbot_section():
    """Display an interactive conservation chatbot assistant."""
    
    # Create a header with green styling for the page
    colored_header(
        label="Conservation Chatbot Assistant",
        description="Get answers to your deforestation and conservation questions",
        color_name="green-70",
    )
    
    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I'm ForestWatch's Conservation Assistant. I can answer questions about deforestation, conservation efforts, and how you can help protect our forests. What would you like to know today?"}
        ]
    
    # Create a container with nice styling for the chat interface
    st.markdown("""
    <div style="
        color: #1b5e20;
        font-size: 1.15rem;
        margin: 15px auto 30px auto;
        max-width: 800px;
        line-height: 1.6;
        text-align: center;
    ">
        Ask me anything about forests, deforestation, conservation methods, or how you can contribute to protecting our planet's valuable ecosystems.
    </div>
    """, unsafe_allow_html=True)
    
    # Create the chat interface
    chat_container = st.container()
    
    # Display chat messages
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: flex-end;
                    margin-bottom: 10px;
                ">
                    <div style="
                        background-color: #e3f2fd;
                        border-radius: 15px 15px 0 15px;
                        padding: 10px 15px;
                        max-width: 80%;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                    ">
                        <p style="margin: 0; color: #1565c0;">{message["content"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: flex-start;
                    margin-bottom: 10px;
                ">
                    <div style="
                        background-color: #e8f5e9;
                        border-radius: 15px 15px 15px 0;
                        padding: 10px 15px;
                        max-width: 80%;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                    ">
                        <p style="margin: 0; color: #2e7d32;">{message["content"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Create forest icon for the chatbot
    forest_icon = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="#4caf50">
        <path d="M12.6 2.86c.23-.01.45 0 .66.03a6.45 6.45 0 0 1 5.2 5.46c.13.82.1 1.65-.1 2.45l.04.03c1.1.15 2.2.64 3.1 1.5l-1.5 1.5c-1-1-2.3-1.5-3.5-1.5s-2.5.5-3.5 1.5l-1.42-1.44c.34-.39.5-.82.5-1.36 0-.56-.16-1.11-.5-1.6-.33-.47-.8-.86-1.4-1.1l-.2-.07c-.14-.04-.29-.04-.44-.04-.3 0-.56.1-.8.31-.24.2-.38.47-.4.77-.04.5.22.93.64 1.22l-.14.14c-1.1.84-2 1.9-2.7 3.12V7.5c0-.83.67-1.5 1.5-1.5h2.02c-.2-.42-.32-.88-.32-1.36 0-.83.35-1.62.9-2.18.56-.54 1.32-.9 2.16-.9Z"/>
        <path d="m7.88 15.93 2.12 2.12c-1 1-2.3 1.5-3.5 1.5s-2.5-.5-3.5-1.5L4.5 16.5a3.5 3.5 0 0 1 3.38-.57ZM13 15.5c0-.83.67-1.5 1.5-1.5h2c.83 0 1.5.67 1.5 1.5v8H13v-8Z"/>
        <path d="M9 18.5c0-.83.67-1.5 1.5-1.5h2c.83 0 1.5.67 1.5 1.5v5H9v-5Z M3 23.5v-2c0-.83.67-1.5 1.5-1.5h2c.83 0 1.5.67 1.5 1.5v2H3Z"/>
    </svg>
    """
    
    # Input for user message with custom styling
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Your message:",
            placeholder="Ask me about forest conservation...",
            label_visibility="collapsed"
        )
        
        cols = st.columns([5, 1])
        with cols[1]:
            submit_button = st.form_submit_button(
                "Send",
                use_container_width=True
            )
    
    # Process user input and generate response when the form is submitted
    if submit_button and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )
        
        # Generate response
        response = generate_response(user_input)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append(
            {"role": "assistant", "content": response}
        )
        
        # Rerun to display the updated chat
        st.rerun()
    
    # Display informational cards below the chat interface
    st.markdown("## Helpful Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background-color: #f1f8e9; 
            border-radius: 12px; 
            border-left: 5px solid #43a047;
            padding: 20px 25px; 
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            margin-bottom: 20px;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="margin-right: 15px;">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40" fill="#4caf50">
                        <path d="M12,3C7,3 3,7 3,12C3,17 7,21 12,21C17,21 21,17 21,12C21,7 17,3 12,3M12,19C8.1,19 5,15.9 5,12C5,8.1 8.1,5 12,5C15.9,5 19,8.1 19,12C19,15.9 15.9,19 12,19M11,7H13V13H11V7M11,15H13V17H11V15Z" />
                    </svg>
                </div>
                <div>
                    <h3 style="margin: 0; color: #2e7d32; font-size: 20px; font-weight: 600;">Forest Facts</h3>
                    <p style="margin: 5px 0 0 0; color: #2e7d32; opacity: 0.9; font-size: 15px;">Key information about global forests</p>
                </div>
            </div>
            <div style="margin-top: 15px; color: #2e7d32;">
                <ul style="padding-left: 20px; margin-top: 0;">
                    <li style="margin-bottom: 8px;">Forests cover about 31% of the world's land surface</li>
                    <li style="margin-bottom: 8px;">Over 1.6 billion people rely on forests for their livelihoods</li>
                    <li style="margin-bottom: 8px;">Forests are home to 80% of terrestrial biodiversity</li>
                    <li style="margin-bottom: 8px;">We lose approximately 4.7 million hectares of forest annually</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background-color: #e8f5e9; 
            border-radius: 12px; 
            border-left: 5px solid #2e7d32;
            padding: 20px 25px; 
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            margin-bottom: 20px;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="margin-right: 15px;">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40" fill="#2e7d32">
                        <path d="M17,4V10L15,8L13,10V4H9V20H11V12L13,10L15,12V20H17V4H21V20H23V4C23,2.89 22.1,2 21,2H8C6.89,2 6,2.89 6,4V12H4V20H6V22H8V20H12V22H14V20H18V22H20V20H23V22H19V20Z" />
                    </svg>
                </div>
                <div>
                    <h3 style="margin: 0; color: #2e7d32; font-size: 20px; font-weight: 600;">Common Questions</h3>
                    <p style="margin: 5px 0 0 0; color: #2e7d32; opacity: 0.9; font-size: 15px;">Topics our chatbot can help with</p>
                </div>
            </div>
            <div style="margin-top: 15px; color: #2e7d32;">
                <ul style="padding-left: 20px; margin-top: 0;">
                    <li style="margin-bottom: 8px;">What are the main causes of deforestation?</li>
                    <li style="margin-bottom: 8px;">How does deforestation affect climate change?</li>
                    <li style="margin-bottom: 8px;">What conservation efforts are most effective?</li>
                    <li style="margin-bottom: 8px;">How can I personally help protect forests?</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a disclaimer at the bottom
    st.markdown("""
    <div style="
        font-size: 0.8rem;
        color: #666;
        text-align: center;
        margin-top: 30px;
        padding: 10px;
        border-top: 1px solid #eee;
    ">
        <p>This conservation chatbot provides general information based on current scientific understanding and conservation best practices. For specific advice, please consult with environmental professionals or organizations.</p>
    </div>
    """, unsafe_allow_html=True)

def generate_response(user_input):
    """
    Generate a response based on user input.
    
    Parameters:
    -----------
    user_input : str
        The user's input text
        
    Returns:
    --------
    str
        The chatbot's response
    """
    # Convert input to lowercase for easier matching
    user_input_lower = user_input.lower()
    
    # Check for different types of questions or keywords and provide appropriate responses
    
    # Deforestation causes
    if any(keyword in user_input_lower for keyword in ["cause", "reason", "why deforestation", "what causes"]):
        return """
        The main causes of deforestation include:
        
        1. **Agricultural expansion** - Clearing forests for crops (like soy and palm oil) and cattle ranching
        2. **Logging** - Both legal and illegal timber harvesting
        3. **Infrastructure development** - Roads, dams, mines, and urban expansion
        4. **Forest fires** - Both natural and human-caused
        5. **Climate change** - Increasing drought and temperature stress
        
        The drivers vary by region. In the Amazon, cattle ranching and soy production are major factors. In Southeast Asia, palm oil and rubber plantations are significant contributors.
        """
    
    # Climate impact
    elif any(keyword in user_input_lower for keyword in ["climate", "global warming", "carbon", "emission", "greenhouse"]):
        return """
        Forests and climate change are deeply connected:
        
        • Forests absorb about 2.6 billion tons of CO₂ annually - about 1/3 of fossil fuel emissions
        • Deforestation accounts for about 10% of global greenhouse gas emissions
        • When forests are cut or burned, stored carbon is released into the atmosphere
        • Beyond carbon, forests regulate water cycles and help cool the planet through evapotranspiration
        • They also provide resilience against climate extremes like floods and droughts
        
        Protecting and restoring forests is considered one of the most cost-effective climate solutions available.
        """
    
    # Personal action
    elif any(keyword in user_input_lower for keyword in ["help", "what can i do", "personal", "individual", "action", "contribute"]):
        return """
        Here are effective ways you can help protect forests:
        
        1. **Consumer choices**: 
           - Choose FSC-certified wood and paper products
           - Avoid products with palm oil or choose RSPO-certified sustainable palm oil
           - Reduce beef consumption or choose sustainably raised beef
        
        2. **Support conservation**:
           - Donate to reputable forest conservation organizations
           - Support indigenous land rights (indigenous-managed forests have lower deforestation rates)
           - Advocate for stronger forest protection policies
        
        3. **Direct action**:
           - Participate in tree planting initiatives
           - Support reforestation projects through verified carbon offset programs
           - Get involved in community forest protection efforts
        
        Every action matters, and combining personal choices with support for systemic change has the most impact!
        """
    
    # Conservation methods
    elif any(keyword in user_input_lower for keyword in ["conservation", "protect", "preserve", "save forest", "restoration"]):
        return """
        Effective forest conservation approaches include:
        
        1. **Protected areas** - National parks and reserves with legal protection
        2. **Indigenous stewardship** - Supporting indigenous peoples' management of their forest lands
        3. **Sustainable forestry** - FSC certification and reduced-impact logging
        4. **Reforestation and restoration** - Tree planting and assisted natural regeneration
        5. **REDD+ programs** - Reducing Emissions from Deforestation and Degradation
        6. **Sustainable supply chains** - Certification for products like timber, palm oil, soy, and beef
        7. **Land use planning** - Smart policies that direct development away from critical forests
        
        The most successful conservation combines multiple strategies and engages all stakeholders - from governments to local communities.
        """
    
    # Biodiversity
    elif any(keyword in user_input_lower for keyword in ["biodiversity", "wildlife", "species", "animals", "plants", "ecosystem"]):
        return """
        Forests are biodiversity powerhouses:
        
        • Tropical forests host 50-80% of the world's terrestrial biodiversity
        • A single hectare of rainforest can contain over 750 tree species and thousands of animal species
        • Many species are found nowhere else (endemic) and are highly vulnerable to forest loss
        • Forests provide crucial habitat for 80% of amphibian species, 75% of bird species, and 68% of mammal species
        
        When forests disappear, we don't just lose trees - we lose intricate ecosystems developed over millions of years, with many species going extinct before they're even discovered. Forests also contain vast genetic resources, including potential medicines and other valuable compounds.
        """
    
    # Economic value
    elif any(keyword in user_input_lower for keyword in ["economic", "money", "valuable", "worth", "value"]):
        return """
        Forests have immense economic value:
        
        • The formal forest sector contributes about $600 billion annually to global GDP (0.8%)
        • Forests directly support livelihoods for 1.6 billion people worldwide
        • The value of "forest ecosystem services" (clean water, carbon storage, flood control, etc.) is estimated at $7-16 trillion annually
        • Ecotourism in forest regions generates billions in revenue
        • Over 25% of modern medicines originated from forest plants
        
        However, much of forests' true value is "invisible" in economic terms. Markets typically value timber and cleared land, but not the crucial ecosystem services that intact forests provide - creating economic incentives for deforestation.
        """
    
    # Forest types
    elif any(keyword in user_input_lower for keyword in ["types", "kind of forest", "forest type", "different forest"]):
        return """
        Major forest types include:
        
        1. **Tropical rainforests** - Warm, wet forests near the equator (Amazon, Congo Basin, Southeast Asia)
        2. **Temperate deciduous forests** - Moderate climate forests that shed leaves seasonally (Eastern US, Europe, East Asia)
        3. **Temperate coniferous forests** - Pine, fir and other evergreen forests (Pacific Northwest, Scandinavia)
        4. **Boreal forests/Taiga** - Northern forests of cold-adapted conifers (Canada, Russia, Scandinavia)
        5. **Mediterranean forests** - Drought-adapted woodlands in Mediterranean climates
        6. **Tropical dry forests** - Forests with distinct wet and dry seasons
        7. **Mangrove forests** - Coastal forests adapted to saltwater environments
        
        Each forest type has unique ecology, biodiversity, and conservation challenges.
        """
    
    # Data and statistics
    elif any(keyword in user_input_lower for keyword in ["statistics", "data", "numbers", "rate", "percentage", "how much"]):
        return """
        Key forest statistics:
        
        • Global forest cover: 4.06 billion hectares (31% of land area)
        • Annual deforestation: 4.7 million hectares (net loss, accounting for planted forests)
        • Primary forest loss: 10 million hectares annually
        • Forest distribution: Tropical (45%), Boreal (27%), Temperate (16%), Subtropical (11%)
        • Countries with most forest: Russia, Brazil, Canada, US, China
        • Countries with highest deforestation rates: Brazil, DR Congo, Indonesia, Bolivia, Malaysia
        • Protected forests: 18% of global forests are in protected areas
        
        While global deforestation rates have declined compared to the 1990s, we're still losing forests at an alarming rate, especially primary forests with irreplaceable ecological value.
        """
    
    # Reforestation/tree planting
    elif any(keyword in user_input_lower for keyword in ["reforestation", "tree planting", "plant trees", "restore", "regrow"]):
        return """
        Reforestation and restoration insights:
        
        • The world has pledged to restore 350 million hectares of forest by 2030 (Bonn Challenge)
        • Natural forest regeneration is often more effective than tree planting, when possible
        • Successful reforestation requires planting the right species in the right places
        • "Tree planting" alone isn't always effective - long-term management is crucial
        • Monoculture plantations don't provide the same ecological benefits as diverse forests
        • The most effective restoration engages local communities and addresses the underlying causes of deforestation
        
        While tree planting gets a lot of attention, protecting existing forests is generally more effective for climate, biodiversity, and ecosystem services. The best approach is to protect existing forests while restoring degraded areas.
        """
    
    # Regional forests
    elif "amazon" in user_input_lower:
        return """
        The Amazon rainforest:
        
        • World's largest rainforest: 5.5 million km² across 9 countries (60% in Brazil)
        • Contains 10% of all known species on Earth
        • Creates its own rainfall through evapotranspiration - "flying rivers"
        • Has lost about 17% of its original extent, with another 17% degraded
        • Scientists warn of a potential "tipping point" at 20-25% deforestation, which could transform parts of the forest to savanna
        • Deforestation is primarily driven by cattle ranching, soy production, and infrastructure
        • Home to about 30 million people, including over 350 indigenous groups
        
        The Amazon plays a crucial role in regulating South American climate and is one of Earth's most important carbon sinks.
        """
    elif any(keyword in user_input_lower for keyword in ["borneo", "southeast asia", "indonesia", "malaysia"]):
        return """
        Southeast Asian forests (including Borneo):
        
        • Some of the oldest rainforests on Earth (130+ million years old)
        • Exceptional biodiversity: 15,000 plant species, 450+ mammals, 600+ birds
        • Home to iconic species like orangutans, tigers, elephants, and rhinos
        • Have lost over 50% of original forest cover (among the highest rates globally)
        • Primary drivers: palm oil, pulp and paper, rubber plantations, and logging
        • High carbon density, particularly in peatlands (crucial for climate mitigation)
        • Significant indigenous populations including Dayak peoples in Borneo
        
        Conservation challenges include rapid development, complex land tenure, and governance issues across multiple countries.
        """
    elif any(keyword in user_input_lower for keyword in ["congo", "africa", "african forest"]):
        return """
        The Congo Basin forests:
        
        • Second-largest tropical rainforest after the Amazon (1.5-2 million km²)
        • Spans 6 countries with Democratic Republic of Congo containing 60%
        • Home to 10,000+ plant species, 1,000+ bird species, and 400+ mammal species
        • Iconic wildlife includes forest elephants, gorillas, chimpanzees, and okapi
        • Currently has lower deforestation rates than Amazon or Southeast Asia
        • Growing pressures from logging, mining, agriculture, and charcoal production
        • Around 80 million people depend on these forests for their livelihoods
        • Faces significant challenges from political instability and governance issues
        
        The Congo Basin is sometimes called "Africa's lung" and plays a critical role in regional climate regulation.
        """
    elif any(keyword in user_input_lower for keyword in ["boreal", "taiga", "northern forest", "russia", "canada"]):
        return """
        Boreal forests (Taiga):
        
        • World's largest terrestrial ecosystem, covering 11% of Earth's land area
        • Stretches across Canada, Alaska, Russia, and Scandinavia
        • Dominated by coniferous trees adapted to cold conditions
        • Lower biodiversity than tropical forests but huge carbon storage
        • Contains 30-40% of global terrestrial carbon, much in soils and peat
        • Major threats include climate change (warming faster than global average), wildfires, logging, and oil/gas development
        • Less publicized than tropical deforestation but increasingly vulnerable
        
        As the climate warms, boreal forests face dramatic changes, with permafrost thaw potentially releasing massive amounts of stored carbon.
        """
    
    # Indigenous peoples
    elif any(keyword in user_input_lower for keyword in ["indigenous", "native", "tribe", "local people", "community"]):
        return """
        Indigenous peoples and forests:
        
        • Indigenous territories contain about 36% of the world's intact forests
        • Research shows deforestation rates are 2-3x lower in indigenous territories
        • Indigenous peoples make up 5% of the world's population but protect 80% of global biodiversity
        • Traditional knowledge includes sustainable forest management practices developed over centuries
        • Many indigenous groups face threats from land encroachment, violence, and rights violations
        • Recognizing indigenous land rights is increasingly acknowledged as an effective conservation strategy
        • The UN Declaration on the Rights of Indigenous Peoples (UNDRIP) affirms their rights to lands and resources
        
        Supporting indigenous forest stewardship combines human rights advancement with effective conservation outcomes.
        """
    
    # Forest fires
    elif any(keyword in user_input_lower for keyword in ["fire", "wildfire", "burning", "flame"]):
        return """
        Forest fires and deforestation:
        
        • Some forest ecosystems are fire-adapted and require periodic fires for health
        • However, human-caused fires are increasing in frequency and severity
        • In tropical forests, fires are often used to clear land after logging
        • Climate change is creating hotter, drier conditions that increase fire risk
        • Once burned, forests become more vulnerable to future fires (feedback loop)
        • Satellite monitoring now provides near-real-time fire detection
        • Fire management approaches vary from complete suppression to prescribed burning
        
        In places like the Amazon, fires are rarely natural and almost always indicate human-driven deforestation. In contrast, some temperate and boreal forests evolved with natural fire cycles.
        """
    
    # Policy and governance
    elif any(keyword in user_input_lower for keyword in ["policy", "law", "government", "regulation", "agreement"]):
        return """
        Forest policy and governance:
        
        • International frameworks include:
          - UN Framework Convention on Climate Change (UNFCCC)
          - Convention on Biological Diversity (CBD)
          - UN Forum on Forests (UNFF)
          - REDD+ (Reducing Emissions from Deforestation and Degradation)
        
        • Key policy approaches:
          - Protected area designation
          - Land tenure reform and indigenous rights recognition
          - Payments for ecosystem services
          - Timber legality verification
          - Supply chain regulations and transparency
          - Moratoria on forest conversion
        
        Effective forest governance requires addressing corruption, improving enforcement, securing indigenous rights, and integrating forest protection into economic development models.
        """
    
    # Greeting
    elif any(keyword in user_input_lower for keyword in ["hello", "hi", "hey", "greetings"]):
        return "Hello! I'm here to provide information about forests, deforestation, and conservation. What would you like to know about today?"
    
    # About the chatbot
    elif any(keyword in user_input_lower for keyword in ["who are you", "what are you", "about you", "your purpose", "chatbot"]):
        return "I'm the ForestWatch Conservation Assistant, designed to provide information about deforestation, forest conservation, and how individuals can take action to protect our forests. I can answer questions about causes of deforestation, impacts on climate and biodiversity, effective conservation strategies, and ways you can help. How can I assist you today?"
    
    # Gratitude
    elif any(keyword in user_input_lower for keyword in ["thanks", "thank you", "appreciate", "helpful"]):
        return "You're welcome! I'm glad I could help. If you have any other questions about forests and conservation, feel free to ask. Every person who learns more about our forests can make a positive difference!"
    
    # Default response for unrecognized inputs
    else:
        return """
        I'm not sure I understand your question fully. I can provide information about:
        
        • Causes and impacts of deforestation
        • Climate change connections
        • Biodiversity and ecosystem services
        • Forest types and regions (Amazon, Borneo, Congo, etc.)
        • Conservation strategies and solutions
        • Ways individuals can help
        • Forest statistics and trends
        
        Could you rephrase your question or specify which aspect of forest conservation you're interested in?
        """