import streamlit as st
from streamlit_extras.colored_header import colored_header
import random

def show_chatbot_button():
    """Display a floating chatbot button at the bottom right that opens a dialog."""
    
    # Initialize chat history in session state if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I'm ForestWatch's Conservation Assistant. I can answer questions about deforestation, conservation efforts, and how you can help protect our forests. What would you like to know today?"}
        ]
    
    # Initialize dialog visibility state
    if 'show_chat_dialog' not in st.session_state:
        st.session_state.show_chat_dialog = False
    
    # Add floating button styles
    st.markdown("""
    <style>
    .chat-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #4CAF50;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        z-index: 9999;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    
    .chat-dialog {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 350px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 9998;
        overflow: hidden;
    }
    
    .chat-header {
        background-color: #2E7D32;
        color: white;
        padding: 10px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 10px 10px 0 0;
    }
    
    .chat-header h3 {
        margin: 0;
        font-size: 16px;
    }
    
    .chat-body {
        height: 300px;
        overflow-y: auto;
        padding: 15px;
    }
    
    .user-message {
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .assistant-message {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin-bottom: 10px;
        max-width: 80%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a container for the button
    button_container = st.container()
    
    # Only show the button if the dialog is not open
    if not st.session_state.show_chat_dialog:
        with button_container:
            # Place the button in the bottom right corner
            if st.button("🌳", key="open_chat"):
                st.session_state.show_chat_dialog = True
                st.rerun()
    
    # Show chat dialog if state is true
    if st.session_state.show_chat_dialog:
        # Create a container for the dialog
        chat_container = st.container()
        
        with chat_container:
            # Chat dialog header
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown("### 🌳 Conservation Assistant")
            with col2:
                if st.button("✕", key="close_chat"):
                    st.session_state.show_chat_dialog = False
                    st.rerun()
            
            # Display chat messages
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="assistant-message">
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show suggested questions if this is a new chat
            if len(st.session_state.chat_history) == 1:
                st.markdown("<p style='color: #666; font-size: 0.9em;'>Suggested questions:</p>", unsafe_allow_html=True)
                
                suggested_questions = [
                    "What are the main causes of deforestation?",
                    "How does deforestation affect climate change?",
                    "What can I do to help protect forests?",
                    "Tell me about biodiversity in forests",
                    "What conservation methods are most effective?"
                ]
                
                for question in suggested_questions:
                    if st.button(question, key=f"suggested_{question}"):
                        # Add user question to chat history
                        st.session_state.chat_history.append(
                            {"role": "user", "content": question}
                        )
                        
                        # Generate response and add to chat history
                        response = generate_response(question)
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": response}
                        )
                        
                        # Rerun to update the UI
                        st.rerun()
            
            # Input for user messages
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_input(
                    "Your message:",
                    key="user_input",
                    placeholder="Ask me about forest conservation...",
                    label_visibility="collapsed"
                )
                
                cols = st.columns([5, 1])
                with cols[1]:
                    submit_button = st.form_submit_button("Send")
            
            # Process user input
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
                
                # Rerun to update the UI
                st.rerun()

def chatbot_section(as_dialog=False):
    """Display an interactive conservation chatbot assistant."""
    
    # Create a header only if not in dialog mode
    if not as_dialog:
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
    
    # Display chat history
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
    
    # Input for user messages
    with st.form(key="chat_form_page", clear_on_submit=True):
        user_input = st.text_input(
            "Your message:",
            key="user_input_page",
            placeholder="Ask me about forest conservation...",
            label_visibility="collapsed"
        )
        
        cols = st.columns([5, 1])
        with cols[1]:
            submit_button = st.form_submit_button("Send")
    
    # Process user input
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
        
        # Rerun to update the UI
        st.rerun()

def generate_response(user_input):
    """Generate a response based on user input with AI-like qualities."""
    
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