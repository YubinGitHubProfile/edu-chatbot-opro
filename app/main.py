import streamlit as st
from models.gemini_flash_client import GeminiFlashClient
from optimizer.opro_engine import OproEngine

st.set_page_config(page_title="OPro-Gemini Chatbot Demo", layout="centered")
st.title("OPro-Gemini Chatbot Demo")

# Sidebar for API key and model selection
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
model_version = st.sidebar.selectbox("Gemini Flash Model", ["gemini-2.0-flash", "gemini-2.5-flash"], index=1)

# Prompt selection
st.sidebar.header("Prompt Selection")
prompt_type = st.sidebar.radio("Prompt Type", ["Base", "Optimized"], index=1)

# Load prompts (for demo, hardcoded; in production, load from files)
base_prompt = "Translate English to French."
optimized_prompt = "You are a helpful assistant. Translate the following English sentence to French, using natural and fluent language."

# Initialize conversation history in session state
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Chat interface
st.subheader("Chat with the Gemini Flash Model")
user_input = st.text_input("Enter your message:")

if st.button("Send") and user_input and api_key:
    flash_client = GeminiFlashClient(api_key=api_key, model_version=model_version)
    with st.spinner("Gemini is thinking..."):
        try:
            base_full_prompt = f"{base_prompt}\nUser: {user_input}"
            opt_full_prompt = f"{optimized_prompt}\nUser: {user_input}"
            base_response = flash_client.generate(base_full_prompt)
            opt_response = flash_client.generate(opt_full_prompt)
            st.session_state['history'].append({
                'user': user_input,
                'base_response': base_response,
                'opt_response': opt_response
            })
        except Exception as e:
            st.error(f"Error: {e}")

# Conversation history display
if st.session_state['history']:
    st.markdown("### Conversation History")
    for turn in st.session_state['history']:
        st.markdown(f"**You:** {turn['user']}")
        st.markdown(f"**Base Prompt:** {turn['base_response']}")
        st.markdown(f"**Optimized Prompt:** {turn['opt_response']}")
        st.markdown("---")

# Prompt comparison table (latest turn)
if st.session_state['history']:
    last_turn = st.session_state['history'][-1]
    st.markdown("### Prompt Comparison Table (Latest)")
    st.table({
        'Prompt Type': ['Base', 'Optimized'],
        'Response': [last_turn['base_response'], last_turn['opt_response']]
    })

st.markdown("---")
st.markdown("Try both base and optimized prompts to compare chatbot performance!")
