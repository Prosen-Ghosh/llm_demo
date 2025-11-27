import streamlit as st
# import os

def init_session():
    """Initialize session state variables"""
    if "llm_api_key" not in st.session_state:
        st.session_state.llm_api_key = None
    
    # Set default API key from environment if available
    # if st.session_state.llm_api_key is None:
    #     env_key = os.environ.get("OPENROUTER_API_KEY")
    #     if env_key:
    #         st.session_state.llm_api_key = env_key