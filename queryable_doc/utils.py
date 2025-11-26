import streamlit as st
import tempfile

def init_session():
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []
    if "chroma_dir" not in st.session_state:
        st.session_state.chroma_dir = tempfile.mkdtemp(prefix="chroma_")
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = None
    if "llm_model" not in st.session_state:
        st.session_state.llm_model = None
    if "chunk_size" not in st.session_state:
        st.session_state.chunk_size = None
    if "chunk_overlap" not in st.session_state:
        st.session_state.chunk_overlap = None
    if "temperature" not in st.session_state:
        st.session_state.temperature = None
    if "top_k" not in st.session_state:
        st.session_state.top_k = None


