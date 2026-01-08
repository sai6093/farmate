import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = "" # Or use st.secrets for deployment

# Configure Gemini
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# System Prompt - THIS IS THE MOST IMPORTANT PART FOR YOUR PROJECT SCOPE
SYSTEM_INSTRUCTION = """
You are the 'Smart Agriculture Crop Process Explainer Bot'. 
Your sole purpose is to educate users on the general processes of farming and crop lifecycles.

STRICT GUIDELINES:
1. Explain stages like Sowing, Irrigation, Harvesting, and Storage clearly and simply.
2. DO NOT provide specific fertilizer, pesticide, or chemical treatment recommendations.
3. DO NOT provide yield predictions or financial forecasts for crops.
4. If a user asks for treatments or yield predictions, politely explain that you are an 
   educational tool and cannot provide agricultural advice or forecasts.
5. Use a helpful, encouraging tone suitable for farmers and students.
6. Use bullet points for readability.
"""

# Initialize Gemini Flash Model
model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction=SYSTEM_INSTRUCTION
)

# Streamlit UI Configuration
st.set_page_config(page_title="Agri-Process Explainer", page_icon="🌱")
st.title("🌱 Smart Agriculture Crop Process Explainer")
st.markdown("Learn about the lifecycle of crops and modern farming processes.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about crop growth, irrigation, or harvesting..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Generate content using Gemini
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar Info
st.sidebar.header("About the Bot")
st.sidebar.info(
    "This AI assistant explains farming stages like:\n"
    "- 🌾 Sowing & Preparation\n"
    "- 💧 Irrigation Cycles\n"
    "- 🚜 Harvesting Process\n"
    "- 🏠 Storage Practices"
)
st.sidebar.warning(
    "Note: This bot does not provide chemical recommendations or yield forecasts."
)
