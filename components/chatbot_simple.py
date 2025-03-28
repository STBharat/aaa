import streamlit as st
from streamlit_extras.colored_header import colored_header
import random

def show_chatbot_button():
    """Display a floating chat button that opens the chatbot dialog."""
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False

    # Add the floating button styling
    st.markdown("""
    <style>
    .fixed-chat-button {
        position: fixed;
        bottom: 80px;
        right: 80px;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background-color: #4CAF50;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.4);
        cursor: pointer;
        z-index: 999999;
        transition: all 0.3s ease;
    }
    .fixed-chat-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a container for the chat button
    chat_container = st.container()

    with chat_container:
        # Add the floating button with click handler
        st.markdown(f"""
        <div class="fixed-chat-button" onclick="document.getElementById('chat-button-hidden').click()">
            💬
        </div>
        """, unsafe_allow_html=True)

        # Hidden button that gets triggered by the floating button
        if st.button("Chat", key="chat-button-hidden", help="Chat with Conservation Assistant"):
            st.session_state.show_chat = not st.session_state.show_chat
            st.rerun()

    # Display chat if state is true
    if st.session_state.show_chat:
        chatbot_section(as_dialog=True)

def chatbot_section(as_dialog=False):
    """Display the conservation chatbot interface."""
    if not as_dialog:
        st.header("Conservation Chatbot")

    st.markdown("Ask questions about deforestation and conservation efforts.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about deforestation..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add assistant response
        response = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)

def generate_response(user_input):
    """Generate a response based on user input with AI-like qualities."""
    user_input_lower = user_input.lower()
    
    # Handle greetings
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your Forest Conservation Assistant. How can I help you today?"
        
    # Handle deforestation questions
    elif 'deforestation' in user_input_lower:
        return "Deforestation is a major environmental issue. The main causes include agriculture expansion, logging, and urban development. What specific aspect would you like to know more about?"
        
    # Handle conservation questions
    elif 'conservation' in user_input_lower:
        return "Forest conservation involves protecting forests from destruction and degradation. This can be done through protected areas, sustainable management, and community involvement. Would you like to know specific ways to help?"
        
    # Handle climate related questions
    elif any(word in user_input_lower for word in ['climate', 'warming', 'temperature']):
        return "Forests play a crucial role in regulating climate. They absorb CO2, help maintain rainfall patterns, and provide natural cooling. Deforestation contributes significantly to climate change."
        
    # Handle action questions
    elif any(word in user_input_lower for word in ['help', 'action', 'do', 'can i']):
        return "There are many ways to help protect forests: support conservation organizations, use sustainable products, reduce paper consumption, and spread awareness about forest protection."
        
    # Default response
    return "I can help you with information about deforestation, conservation efforts, climate impacts, and ways to protect forests. What would you like to know more about?"
    
    # Track conversation context
    if 'conversation_context' not in st.session_state:
        st.session_state.conversation_context = {
            'topics_discussed': [],
            'questions_asked': 0,
            'regions_mentioned': []
        }
    
    # Update context
    st.session_state.conversation_context['questions_asked'] += 1
    
    # Get personalized greeting based on conversation history
    questions_asked = st.session_state.conversation_context['questions_asked']
    topics_discussed = st.session_state.conversation_context['topics_discussed']
    
    # Create personalized greeting if we've had some conversation already
    personalization = ""
    if questions_asked > 2 and len(topics_discussed) > 0:
        personalization_options = [
            f"I see you're interested in forest conservation topics! ",
            f"Building on our conversation about {topics_discussed[-1]}, ",
            f"Thanks for your continued interest in forests. ",
            f"Great question! "
        ]
        personalization = random.choice(personalization_options)
    
    # Convert input to lowercase for easier matching
    user_input_lower = user_input.lower()
    
    # Check for deforestation causes
    if any(keyword in user_input_lower for keyword in ["cause", "reason", "why", "driver", "what causes"]):
        if "deforestation" in user_input_lower:
            st.session_state.conversation_context['topics_discussed'].append("deforestation_causes")
            return f"""{personalization}The main drivers of deforestation globally are:
            
            • **Agricultural expansion** (70-80% of deforestation): Clearing forests for crops, livestock grazing, and plantations like palm oil, soy, and rubber
            
            • **Commercial logging**: Both legal and illegal timber harvesting that often opens up previously inaccessible forests
            
            • **Infrastructure development**: Road construction, mining, hydroelectric dams, and urban expansion
            
            • **Subsistence farming**: Small-scale agriculture practiced by local communities who clear forest patches for cultivation
            
            The underlying causes are often complex and interconnected, including economic pressures, weak governance, unclear land tenure, corruption, and market demands for commodities.
            
            Different regions face different primary drivers - in the Amazon, cattle ranching and soy production are major factors, while in Southeast Asia, palm oil plantations are a significant cause.
            
            Would you like to know more about solutions to address these drivers?"""
    
    # Check for climate change queries
    elif any(keyword in user_input_lower for keyword in ["climate", "warming", "carbon", "temperature"]):
        st.session_state.conversation_context['topics_discussed'].append("climate_impact")
        return f"""{personalization}Forests and climate change are deeply interconnected:
        
        • Forests are crucial **carbon sinks**, absorbing about 2.6 billion tons of carbon dioxide annually - nearly one-third of emissions from burning fossil fuels
        
        • When forests are destroyed, this stored carbon is released back into the atmosphere. Deforestation contributes approximately 10% of global greenhouse gas emissions
        
        • Beyond carbon storage, forests regulate regional rainfall patterns and temperature. Massive deforestation in the Amazon, for instance, is altering rainfall patterns across South America
        
        • Forests also help communities adapt to climate change impacts by preventing soil erosion, reducing flooding, and providing natural cooling
        
        The relationship works both ways - as climate change accelerates, forests face increased threats from droughts, wildfires, pest outbreaks, and extreme weather events.
        
        This creates a dangerous feedback loop: climate change damages forests, reducing their capacity to mitigate climate change, which in turn leads to more forest degradation.
        
        What aspect of the forest-climate relationship would you like to explore further?"""
    
    # Check for helping/action queries
    elif any(keyword in user_input_lower for keyword in ["help", "action", "protect", "save", "conserve", "preservation", "contribute"]):
        st.session_state.conversation_context['topics_discussed'].append("individual_action")
        return f"""{personalization}There are many meaningful ways you can help protect forests:
        
        **In your daily life:**
        • Choose products with credible sustainability certifications (FSC for wood/paper, RSPO for palm oil)
        • Reduce paper consumption and recycle paper products
        • Minimize beef consumption from unsustainable sources
        • Support brands committed to zero-deforestation supply chains
        
        **Beyond personal choices:**
        • Donate to effective forest conservation organizations (like Rainforest Alliance, Cool Earth, or Amazon Conservation Team)
        • Participate in tree planting initiatives in your community
        • Advocate for stronger forest protection policies
        • Support indigenous communities' land rights - indigenous-managed forests show lower deforestation rates
        
        **If you enjoy technology:**
        • Contribute to citizen science projects monitoring forest health
        • Use apps like Forest Watcher to report illegal deforestation
        
        Even small actions collectively make a difference. Would you like specific recommendations for organizations doing effective forest conservation work?"""
    
    # Check for biodiversity queries
    elif any(keyword in user_input_lower for keyword in ["biodiversity", "species", "wildlife", "animals", "plants", "ecosystem"]):
        st.session_state.conversation_context['topics_discussed'].append("biodiversity")
        return f"""{personalization}Forests are extraordinarily rich biodiversity hotspots:
        
        • **Incredible diversity**: Tropical forests alone host approximately 50% of Earth's plant and animal species despite covering just 6% of land surface
        
        • **Layered habitats**: The complex vertical structure of forests (forest floor, understory, canopy, emergent layer) creates countless ecological niches
        
        • **Specialized relationships**: Many forest species have co-evolved in intricate relationships - like specific pollinators for certain plants
        
        • **Undiscovered species**: Scientists estimate we've identified only a fraction of forest species, particularly insects and microorganisms
        
        Deforestation's impact on biodiversity is profound:
        • Habitat loss and fragmentation disrupt migration routes and breeding patterns
        • Edge effects expose interior forest species to new conditions they can't tolerate
        • Local extinctions can trigger cascade effects through food webs
        
        The biodiversity within forests also provides humanity with invaluable services - from medicines (25% of modern pharmaceuticals originate from rainforest plants) to pest control and pollination.
        
        Is there a particular forest ecosystem or aspect of forest biodiversity you'd like to learn more about?"""
    
    # Check for conservation methods
    elif any(keyword in user_input_lower for keyword in ["conservation", "method", "approach", "strategy", "solution", "effective"]):
        st.session_state.conversation_context['topics_discussed'].append("conservation_methods")
        return f"""{personalization}The most effective forest conservation approaches combine multiple strategies:
        
        **Protected Areas & Indigenous Stewardship**
        • Well-managed protected areas with adequate funding and enforcement
        • Recognition of indigenous land rights - indigenous territories show significantly lower deforestation rates than unprotected areas
        
        **Economic Approaches**
        • Payment for Ecosystem Services (PES) programs that compensate communities for maintaining forests
        • REDD+ initiatives (Reducing Emissions from Deforestation and Degradation)
        • Sustainable forestry certification systems like FSC
        
        **Policy & Governance**
        • Stronger environmental laws with effective enforcement
        • Transparent monitoring systems using satellite technology
        • Zero-deforestation commitments from companies and governments
        
        **Sustainable Development**
        • Agroforestry systems that integrate trees with agriculture
        • Community-based forest management
        • Alternative livelihoods that don't require forest clearing
        
        **Restoration**
        • Large-scale reforestation and forest landscape restoration
        • Natural regeneration approaches rather than plantation-style replanting
        
        Effective forest governance requires addressing corruption, improving enforcement, securing indigenous rights, and integrating forest protection into economic development models.
        """
    
    # When user says thank you or goodbye
    elif any(keyword in user_input_lower for keyword in ["bye", "goodbye", "thank you", "thanks", "farewell"]):
        return f"""You're very welcome! I'm glad I could help with information about forest conservation. Remember that every action to protect and restore forests makes a difference, no matter how small.
        
        Feel free to return anytime you have more questions about forests, deforestation, or conservation efforts. Together, we can work toward a future with healthy forests for generations to come!
        
        Have a wonderful day! 🌳
        """
    
    # For questions about the chatbot itself
    elif any(keyword in user_input_lower for keyword in ["you", "chatbot", "assistant", "ai", "who are you", "what are you"]):
        return f"""I'm the ForestWatch Conservation Assistant, designed to provide information about forests, deforestation patterns, conservation strategies, and ways to help protect these vital ecosystems.
        
        I can answer questions about different forest regions (like the Amazon, Congo Basin, or Southeast Asian forests), discuss how deforestation affects climate change and biodiversity, explain conservation approaches, and suggest ways you can contribute to forest protection.
        
        I'm here to make forest science and conservation information more accessible. While I'm not a human expert, I aim to provide accurate, up-to-date information to help people understand and appreciate the importance of forests.
        
        What would you like to know about forest conservation today?
        """
    
    # General forest question
    elif any(keyword in user_input_lower for keyword in ["forest", "tree", "woodland", "jungle"]):
        st.session_state.conversation_context['topics_discussed'].append("general_forests")
        return f"""{personalization}Forests are remarkable ecosystems that cover about 31% of Earth's land surface and are essential for all life on our planet. They:
        
        • Create habitat for approximately 80% of the world's terrestrial biodiversity, from tiny insects to large mammals
        
        • Act as massive carbon sinks, absorbing about 2.6 billion tons of CO₂ annually, helping mitigate climate change
        
        • Regulate water cycles - forests act like giant sponges, preventing flooding during heavy rainfall and releasing water during dry periods
        
        • Stabilize soil and prevent erosion, protecting watersheds that provide drinking water to billions of people
        
        • Support the livelihoods of about 1.6 billion people globally, including countless indigenous communities with deep cultural connections to forest lands
        
        • Provide countless resources we rely on daily, from timber and paper to medicines, foods, and fibers
        
        Despite their importance, we're losing about 4.7 million hectares of forest annually to deforestation - roughly equivalent to losing a football field of forest every second.
        
        Is there a particular aspect of forests you'd like to explore further?
        """
    
    # Detect questions about the dashboard or app
    elif any(keyword in user_input_lower for keyword in ["dashboard", "app", "application", "website", "platform", "tool", "software"]):
        st.session_state.conversation_context['topics_discussed'].append("dashboard")
        return f"""{personalization}The ForestWatch dashboard is designed to make complex deforestation data more accessible and actionable through several key features:
        
        • **Interactive mapping**: Visualize forest cover, deforestation hotspots, and conservation areas through layered maps you can explore by region.
        
        • **Before-and-after analysis**: Upload satellite images to see changes over time with automated detection of forest loss and detailed metrics.
        
        • **Time-series visualization**: Track forest cover changes over decades for any selected region to identify trends and patterns.
        
        • **Real-time alerts**: Monitor active deforestation through recent satellite detections, particularly useful for conservation organizations.
        
        • **Global forest health**: Explore interactive indicators of forest health across different regions and compare trends between countries.
        
        • **Educational resources**: Access information about conservation efforts and ways to get involved in forest protection.
        
        You can navigate between these features using the sidebar menu. Each section provides different insights into deforestation patterns and potential solutions.
        
        Is there a specific feature of the dashboard you're interested in exploring more deeply?
        """
    
    # Default response for anything else - make it vary slightly for more natural feel
    else:
        # Make default responses vary slightly to feel more natural
        responses = [
            f"That's an interesting question about forests or conservation. I can provide information about deforestation causes, climate impacts, biodiversity, conservation methods, economic value of forests, and ways you can help protect these vital ecosystems. Could you clarify which aspect you'd like to learn more about?",
            
            f"I'd be happy to discuss that aspect of forest conservation. My knowledge covers deforestation drivers, climate connections, biodiversity impacts, conservation strategies, and actions individuals can take to help. To provide the most relevant information, could you specify which area interests you most?",
            
            f"Great question! I can share information about forest types, regional conservation challenges, deforestation statistics, restoration approaches, and the ecological importance of forests. To help focus my response, could you let me know which specific aspect of forests or conservation you're curious about?"
        ]
        
        return random.choice(responses)

import random