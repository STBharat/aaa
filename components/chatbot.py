import streamlit as st
from streamlit_extras.colored_header import colored_header
from PIL import Image
import base64
import io
import random

def show_chatbot_button():
    """Display a floating chatbot button at the bottom right of the dashboard 
    that opens an inline chat dialog rather than redirecting to a new page."""
    
    # Initialize session state for chat visibility and history if not already set
    if 'show_chatbot_dialog' not in st.session_state:
        st.session_state.show_chatbot_dialog = False
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I'm ForestWatch's Conservation Assistant. I can answer questions about deforestation, conservation efforts, and how you can help protect our forests. What would you like to know today?"}
        ]
    
    # Add a fixed position button in the bottom right
    # First add the CSS for a nice floating button
    st.markdown("""
    <style>
    /* Floating chat button styles */
    .fixed-chat-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #4CAF50;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        cursor: pointer;
        z-index: 9999;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    
    /* Chat dialog styles */
    .chat-dialog {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 350px;
        max-height: 500px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 9998;
        overflow: hidden;
    }
    
    /* Overriding some Streamlit button styles for our chatbot */
    div[data-testid="stVerticalBlock"] div.chat-button-override > button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        border: none !important;
    }
    
    div[data-testid="stVerticalBlock"] div.chat-button-override > button:hover {
        background-color: #45a049 !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Only show the button if the dialog is not visible
    if not st.session_state.show_chatbot_dialog:
        # Create a button that looks like a floating button
        st.markdown("""
        <div class="fixed-chat-button" onclick="document.getElementById('chat-button-hidden').click()">
            🌳
        </div>
        """, unsafe_allow_html=True)
        
        # Hidden button that will be clicked by our custom button
        if st.button("Open Chat", key="chat-button-hidden", help="Chat with Conservation Assistant", 
                     style={"display": "none"}):
            st.session_state.show_chatbot_dialog = True
            st.rerun()
    
    # Show chat dialog if state is true
    if st.session_state.show_chatbot_dialog:
        # Add specific styling for the chat dialog to make it look like a floating popup
        st.markdown("""
        <style>
        /* Style for the chat dialog to make it look floating */
        div[data-testid="stVerticalBlock"] div.chat-dialog-container {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 8px 26px rgba(0,0,0,0.2);
            border: 1px solid #e0e0e0;
            margin: 0;
            padding: 0;
            max-width: 400px;
            position: fixed;
            bottom: 90px;
            right: 20px;
            z-index: 9998;
            overflow: hidden;
        }
        
        /* Chat header styling */
        .chat-header {
            background-color: #2E7D32;
            color: white;
            padding: 12px 15px;
            margin: 0;
            border-radius: 15px 15px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* Make close button more visible */
        div[data-testid="stVerticalBlock"] div.chat-dialog-container .close-button button {
            background-color: transparent !important;
            color: white !important;
            border: none !important;
            font-size: 20px !important;
            font-weight: bold !important;
            padding: 0 !important;
            width: 30px !important;
            height: 30px !important;
        }
        
        /* Make the chat content scroll if it gets too long */
        div[data-testid="stVerticalBlock"] div.chat-dialog-container .chat-body {
            max-height: 300px;
            overflow-y: auto;
            padding: 15px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Wrap our chat dialog in a container with the special class
        with st.container():
            # This div will be styled with CSS to look like a floating dialog
            st.markdown('<div class="chat-dialog-container">', unsafe_allow_html=True)
            
            # Chat header with close button
            st.markdown("""
            <div class="chat-header">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 18px; margin-right: 8px;">🌳</span>
                    <span style="font-weight: bold;">Conservation Assistant</span>
                </div>
                <div id="close-button-placeholder"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Close button - needs to be a Streamlit button to work
            col1, col2 = st.columns([6, 1])
            with col2:
                with st.container():
                    st.markdown('<div class="close-button">', unsafe_allow_html=True)
                    if st.button("✕", key="close_chat"):
                        st.session_state.show_chatbot_dialog = False
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Chat body will contain all messages
            st.markdown('<div class="chat-body">', unsafe_allow_html=True)
            
            # Display chat messages with custom styling
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
            
            # If this is a new chat (first message only), show suggested questions
            if len(st.session_state.chat_history) == 1:
                st.markdown("""
                <p style="color: #666; font-size: 0.9em; margin-top: 15px;">Suggested questions:</p>
                """, unsafe_allow_html=True)
                
                suggested_questions = [
                    "What are the main causes of deforestation?",
                    "How does deforestation affect climate change?",
                    "What can I do to help protect forests?",
                    "Tell me about biodiversity in forests",
                    "What conservation methods are most effective?"
                ]
                
                for question in suggested_questions:
                    if st.button(question, key=f"suggested_{question}"):
                        # Add user message to chat history
                        st.session_state.chat_history.append(
                            {"role": "user", "content": question}
                        )
                        
                        # Generate response
                        response = generate_response(question)
                        
                        # Add assistant response to chat history
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": response}
                        )
                        
                        # Rerun to display the updated chat
                        st.rerun()
            
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

def chatbot_section(as_dialog=False):
    """
    Display an interactive conservation chatbot assistant.
    
    Parameters:
    -----------
    as_dialog : bool
        If True, display as a compact dialog for embedding elsewhere.
        If False, display as a full page with header and descriptions.
    """
    
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
    
    # Create a container with nice styling for the chat interface (smaller for dialog mode)
    if not as_dialog:
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
    else:
        st.markdown("""
        <div style="
            color: #1b5e20;
            font-size: 0.95rem;
            margin: 5px auto 15px auto;
            max-width: 100%;
            line-height: 1.4;
            text-align: center;
        ">
            Ask me about forests & conservation
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
    
    # Display informational cards below the chat interface - only in full page mode
    if not as_dialog:
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
    Generate a more AI-like response based on user input.
    
    Parameters:
    -----------
    user_input : str
        The user's input text
        
    Returns:
    --------
    str
        The chatbot's response with more natural language and conversational elements
    """
    # Convert input to lowercase for easier matching
    user_input_lower = user_input.lower()
    
    # Track conversation context (would be improved with actual NLP)
    if 'conversation_context' not in st.session_state:
        st.session_state.conversation_context = {
            'topics_discussed': [],
            'questions_asked': 0,
            'regions_mentioned': []
        }
    
    # Update context
    st.session_state.conversation_context['questions_asked'] += 1
    
    # Extract potential topics from user input
    potential_topics = []
    if any(word in user_input_lower for word in ["cause", "reason", "why", "driver"]):
        potential_topics.append("causes")
    if any(word in user_input_lower for word in ["climate", "carbon", "warming", "emission"]):
        potential_topics.append("climate")
    if any(word in user_input_lower for word in ["help", "action", "contribute", "do", "personal"]):
        potential_topics.append("action")
    
    # Add new topics to context
    for topic in potential_topics:
        if topic not in st.session_state.conversation_context['topics_discussed']:
            st.session_state.conversation_context['topics_discussed'].append(topic)
    
    # Track mentioned regions
    regions = ["amazon", "borneo", "congo", "asia", "africa", "europe", "america"]
    for region in regions:
        if region in user_input_lower and region not in st.session_state.conversation_context['regions_mentioned']:
            st.session_state.conversation_context['regions_mentioned'].append(region)
    
    # Personalization elements based on conversation history
    personalization = ""
    if st.session_state.conversation_context['questions_asked'] > 1:
        personalization = "Thanks for your continued interest in forest conservation. "
    if len(st.session_state.conversation_context['topics_discussed']) > 2:
        personalization += "I can see you're curious about multiple aspects of forests! "
    
    # Add occasional references to previous topics for continuity
    continuity = ""
    if len(st.session_state.conversation_context['topics_discussed']) > 1 and random.random() < 0.3:
        prev_topic = random.choice(st.session_state.conversation_context['topics_discussed'][:-1])
        continuity = f"Earlier we talked about {prev_topic} of deforestation. "
    
    # Check for different types of questions or keywords and provide appropriate responses
    
    # Main response generation logic - enhanced for more natural language
    
    # Greeting or introduction
    if any(keyword in user_input_lower for keyword in ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]):
        return f"{personalization}Hello! I'm your ForestWatch Conservation Assistant. I'm here to help with questions about forests, deforestation, conservation efforts, and how we can protect our planet's valuable ecosystems. What would you like to know about today?"
    
    # Deforestation causes
    elif any(keyword in user_input_lower for keyword in ["cause", "reason", "why deforestation", "what causes"]):
        st.session_state.conversation_context['topics_discussed'].append("causes")
        return f"""{personalization}{continuity}The main drivers of deforestation around the world include:

1. **Agricultural expansion** - This is the biggest factor globally, with forests being cleared for crops (especially soy and palm oil) and cattle ranching. In the Amazon, for example, about 80% of deforestation is linked to cattle ranching.

2. **Commercial logging** - Both legal and illegal timber harvesting contribute significantly to forest loss, especially in Southeast Asia and parts of Africa.

3. **Infrastructure development** - Roads, dams, mines, and urban expansion often cut through forests, fragmenting habitats and opening remote areas to further development.

4. **Forest fires** - Both natural and human-caused fires affect millions of hectares annually, with climate change making fire seasons longer and more severe.

5. **Climate change** - Increasing drought and temperature stress are damaging some forests, making them more vulnerable to disease and pests.

The drivers vary significantly by region. Would you like me to elaborate on the deforestation patterns in a specific region like the Amazon, Congo Basin, or Southeast Asia?
        """
    
    # Climate impact
    elif any(keyword in user_input_lower for keyword in ["climate", "global warming", "carbon", "emission", "greenhouse"]):
        st.session_state.conversation_context['topics_discussed'].append("climate")
        return f"""{personalization}{continuity}Forests and climate change are deeply interconnected in ways that make forest conservation one of our most powerful climate solutions:

• Forests function as enormous carbon sinks, absorbing about 2.6 billion tons of CO₂ annually - approximately one-third of fossil fuel emissions worldwide.

• When forests are cut or burned, this carbon is released back into the atmosphere - currently, deforestation accounts for roughly 10% of global greenhouse gas emissions.

• Beyond carbon storage, forests create their own microclimates and regulate water cycles through evapotranspiration, which helps cool the planet. The Amazon rainforest, for instance, generates about 50-75% of its own rainfall through this process!

• Forests also provide natural resilience against climate extremes, reducing flooding, preventing soil erosion, and mitigating drought impacts.

The IPCC and many climate scientists consider protecting existing forests and restoring degraded ones to be among the most cost-effective climate solutions available. Would you like to know more about how forest conservation fits into climate action plans, or perhaps how climate change is affecting forests?
        """
    
    # Personal action
    elif any(keyword in user_input_lower for keyword in ["help", "what can i do", "personal", "individual", "action", "contribute"]):
        st.session_state.conversation_context['topics_discussed'].append("action")
        return f"""{personalization}I'm really glad you're asking about personal actions! Here are effective ways you can help protect forests in your daily life:

1. **Mindful consumption**: 
   - Look for FSC-certified wood and paper products, which ensure sustainable forest management
   - Check for RSPO certification on palm oil products or try to reduce palm oil consumption
   - Consider reducing beef consumption or switching to more sustainably raised options, as cattle ranching is a leading cause of deforestation

2. **Support forest conservation**:
   - Even small donations to reputable organizations like Rainforest Alliance, WWF, or local conservation groups make a difference
   - Support indigenous land rights - areas managed by indigenous communities typically have much lower deforestation rates
   - Use your voice to advocate for stronger forest protection policies with elected officials

3. **Direct participation**:
   - Join or organize tree planting events in your community
   - Consider supporting verified forest carbon offset programs for unavoidable emissions
   - Educate others about forest conservation - awareness is a powerful catalyst for change!

Remember, your individual choices create market demand that companies respond to. When combined with support for systemic change, your actions really do matter! Is there a specific type of action you'd like more details about?
        """
    
    # Conservation methods
    elif any(keyword in user_input_lower for keyword in ["conservation", "protect", "preserve", "save forest", "restoration"]):
        st.session_state.conversation_context['topics_discussed'].append("conservation")
        return f"""{personalization}{continuity}There are several proven approaches to forest conservation that work in different contexts:

1. **Protected areas** - Establishing legally protected forests as national parks, reserves, and wildlife sanctuaries. When well-managed, these are highly effective at preserving biodiversity. Currently about 18% of forests globally have protected status.

2. **Indigenous stewardship** - Supporting indigenous peoples' rights to manage their traditional forest lands. Research consistently shows indigenous-managed forests have equal or lower deforestation rates than conventional protected areas.

3. **Sustainable forestry** - Implementing reduced-impact logging techniques and pursuing FSC certification, which allows for some timber harvesting while maintaining forest ecosystem functions.

4. **Forest restoration** - Reforesting degraded areas through active tree planting or assisted natural regeneration. The global Bonn Challenge aims to restore 350 million hectares by 2030.

5. **REDD+ programs** - "Reducing Emissions from Deforestation and Degradation" programs provide financial incentives to developing countries for preserving their forests.

6. **Supply chain reforms** - Certification systems and zero-deforestation commitments for commodities like timber, palm oil, soy, and beef.

7. **Integrated land use planning** - Developing policies that direct development away from critical forest areas while meeting economic needs.

The most successful conservation approaches combine multiple strategies and engage all stakeholders - from governments to local communities. Would you like to explore any of these approaches in more detail?
        """
    
    # Biodiversity
    elif any(keyword in user_input_lower for keyword in ["biodiversity", "wildlife", "species", "animals", "plants", "ecosystem"]):
        st.session_state.conversation_context['topics_discussed'].append("biodiversity")
        return f"""{personalization}Forests are incredible biodiversity powerhouses - true treasure troves of life:

• Tropical forests alone host 50-80% of the world's terrestrial biodiversity despite covering just about 10% of Earth's land surface.

• The diversity is mind-boggling - a single hectare of rainforest can contain over 750 tree species and thousands of animal species. For perspective, all of North America has about 700 tree species total!

• Many forest species are endemic, meaning they're found nowhere else on Earth. In Madagascar's forests, for example, over 90% of reptiles and amphibians exist nowhere else.

• Forests provide crucial habitat for 80% of amphibian species, 75% of bird species, and 68% of mammal species globally.

When forests disappear, we don't just lose trees - we lose intricate ecological networks that have evolved over millions of years. Many species go extinct before scientists even discover them. We're essentially losing a vast biological library we've barely begun to read.

Forests also contain incredible genetic resources, including compounds for medicine. About 25% of modern pharmaceuticals were originally derived from forest plants. The potential for new discoveries remains enormous if we can protect these ecosystems.

Is there a particular aspect of forest biodiversity that interests you most?
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
    
    # This greeting and about sections are now handled by the main response logic elsewhere
    
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