import streamlit as st
import os
import shutil
from document_handler import process_documents
from chat import get_chat_response, display_chat
from embeddings import split_doc_into_chunk, embedding_and_store

def render_body_content():
    col1, col2 = st.columns([1, 1])
    api_key = st.session_state.openai_api_key
    chunk_size = st.session_state.chunk_size
    chunk_overlap = st.session_state.chunk_overlap

    with col1:
        st.header("📤 Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            type=["pdf", "doc", "docx", "txt"],
            accept_multiple_files=True,
            help="Upload PDF, DOC, DOCX, or TXT files"
        )

        if uploaded_files and st.button("Process Documents", type="primary", use_container_width=True):
            if not api_key:
                st.error("⚠️ Please enter your OpenAI API key in the sidebar first!")
            else:
                with st.spinner("Processing documents..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    all_documents = process_documents(
                        uploaded_files=uploaded_files,
                        status_text=status_text,
                        progress_bar=progress_bar
                    )
                    
                    chunks = split_doc_into_chunk(all_documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    vector_store = embedding_and_store(chunks, api_key=api_key)
                    
                    progress_bar.empty()
                    status_text.text(f"✅ Successfully processed {len(uploaded_files)} file(s) into {len(chunks)} chunks!")

                    if vector_store:
                        st.session_state.vector_store = vector_store
                        st.success("✅ Documents processed successfully!")
                    st.balloons()

    with col2:
        st.header("💬 Ask Questions")
        
        if st.session_state.vector_store is None:
            st.info("👈 Please upload and process documents first!")
        else:
            # Query input
            query = st.text_input(
                "Enter your question:",
                placeholder="What is this document about?",
                key="query_input"
            )
            
            if st.button("Get Answer", type="primary", use_container_width=True) and query:
                if not api_key:
                    st.error("⚠️ Please enter your OpenRouter API key in the sidebar!")
                else:
                    with st.spinner("Searching documents and generating answer..."):
                        try:
                            st.write("🔍 Retrieving relevant chunks...")
                            response = get_chat_response(
                                query,
                                st.session_state.vector_store,
                            )
                            
                            st.write("✅ Response generated!")
                            
                            # Add to chat history
                            st.session_state.chat_history.append({
                                "question": query,
                                "answer": response["answer"],
                                "sources": response.get("context", [])
                            })
                            
                            st.rerun()
                        
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            import traceback
                            st.error(f"Full traceback:\n{traceback.format_exc()}")

    display_chat()