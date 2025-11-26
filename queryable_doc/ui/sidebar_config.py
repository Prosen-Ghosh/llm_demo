import streamlit as st
import os
import shutil
import tempfile

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            help="Enter your OpenRouter API key from https://openrouter.ai/keys"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.session_state.openai_api_key = api_key
        
        st.divider()

        st.subheader("Model Selection")
        llm_model = st.selectbox(
            "Chat Model",
            options=[
                "anthropic/claude-3.5-sonnet",
                "openai/gpt-4o",
                "openai/gpt-4o-mini",
                "google/gemini-pro-1.5",
                "meta-llama/llama-3.1-70b-instruct",
                "qwen/qwen-2.5-72b-instruct",
                "mistralai/mistral-large"
            ],
            index=2,
            help="Select the LLM model for answering questions"
        )
        if llm_model:
            st.session_state.llm_model = llm_model
        st.info("📊 Embedding Model: openai/text-embedding-3-small")
        st.divider()
        
        st.subheader("Document Processing")
        chunk_size = st.slider("Chunk Size", 500, 2000, 1000, 100)
        chunk_overlap = st.slider("Chunk Overlap", 0, 500, 200, 50)
        
        if chunk_size:
            st.session_state.chunk_size = chunk_size

        if chunk_overlap:
            st.session_state.chunk_overlap = chunk_overlap
        st.divider()
        
        st.subheader("Query Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
        top_k = st.slider("Number of Retrieved Chunks", 1, 10, 3, 1)
        
        if top_k:
            st.session_state.top_k = top_k

        if temperature:
            st.session_state.temperature = temperature
            
        st.divider()
        if st.session_state.processed_files:
            st.subheader("📄 Processed Files")
            for file in st.session_state.processed_files:
                st.text(f"✓ {file}")
            
            if st.button("🗑️ Clear All Documents", use_container_width=True):
                # Clean up ChromaDB directory
                if os.path.exists(st.session_state.chroma_dir):
                    shutil.rmtree(st.session_state.chroma_dir)
                    st.session_state.chroma_dir = tempfile.mkdtemp(prefix="chroma_")
                
                st.session_state.vector_store = None
                st.session_state.chat_history = []
                st.session_state.processed_files = []
                st.rerun()

    return llm_model, chunk_size, chunk_overlap, temperature, top_k