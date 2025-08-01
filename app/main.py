import streamlit as st
from models.gemini_flash_client import GeminiFlashClient
from optimizer.opro_engine import OproEngine
import sys
import os
from dotenv import load_dotenv
import importlib.util
import json

# Add parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Load environment variables from .env file
load_dotenv()

# Load config.py
spec = importlib.util.spec_from_file_location("config", os.path.abspath(os.path.join(os.path.dirname(__file__), '../config.py')))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

# Load and merge base and private prompts
base_prompts_path = os.path.join(os.path.dirname(__file__), '../prompts/base_prompts.json')
private_prompts_path = os.path.join(os.path.dirname(__file__), '../prompts/private_prompts.json')
prompt_data = {}
if os.path.exists(base_prompts_path):
    with open(base_prompts_path, 'r', encoding='utf-8') as f:
        prompt_data.update(json.load(f))
if os.path.exists(private_prompts_path):
    with open(private_prompts_path, 'r', encoding='utf-8') as f:
        prompt_data.update(json.load(f))


# Only launch Streamlit UI if enabled in config
if config.USE_STREAMLIT_UI:
    st.set_page_config(page_title="OPro-Gemini Chatbot Demo", layout="centered")
    st.title("OPro-Gemini Chatbot Demo")

    # Sidebar for API key and model selection
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Gemini API Key", type="password")
    model_version = st.sidebar.selectbox("Gemini Flash Model", ["gemini-2.0-flash", "gemini-2.5-flash"], index=1)
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=config.TEMPERATURE, step=0.05)
    num_iterations = st.sidebar.slider("OPro Iterations", min_value=1, max_value=10, value=config.NUM_ITERATIONS, step=1)
    prompt_type = st.sidebar.selectbox("Prompt Type", list(prompt_data.keys()), index=list(prompt_data.keys()).index(config.PROMPT_TYPE))

    # Select prompt from config and JSON
    base_prompt = prompt_data[prompt_type]['prompt']
    optimized_prompt = prompt_data[prompt_type]['prompt']  # For now, use the same; can be extended for optimized

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
                base_response = flash_client.generate(base_full_prompt, temperature=temperature)
                opt_response = flash_client.generate(opt_full_prompt, temperature=temperature)
                st.session_state['history'].append({
                    'user': user_input,
                    'base_response': base_response,
                    'opt_response': opt_response
                })
            except Exception as e:
                st.error(f"Error: {e}")

    # OPro optimization button (optional)
    st.markdown("---")
    if st.button("Run OPro Optimization (Demo)"):
        st.info(f"Running OPro optimization loop for {num_iterations} iteration(s). This may take a while...")
        try:
            # Example: use base_prompt and a few dummy task examples
            task_examples = [
                {"input": "Hello!", "target": "Bonjour!"},
                {"input": "How are you?", "target": "Comment ça va?"}
            ]
            opro_engine = OproEngine(base_prompt, task_examples, num_iterations=num_iterations, api_key=api_key)
            best_prompt = opro_engine.optimize()
            st.success(f"Best prompt found: {best_prompt}")
        except Exception as e:
            st.error(f"OPro optimization failed: {e}")

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
else:
    print("Streamlit UI is disabled. Running in backend-only mode. You can now run backend scripts or OPro optimization from the command line.")
