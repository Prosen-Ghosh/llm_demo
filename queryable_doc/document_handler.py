from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.schema import Document
from typing import List
import streamlit as st
import tempfile
import os

def load_document(file_path: str, file_type: str) -> List[Document]:
    try:
        if file_type == "pdf":
            loader = PyPDFLoader(file_path)
        elif file_type in ["docx", "doc"]:
            loader = Docx2txtLoader(file_path)
        elif file_type == "txt":
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return loader.load()

    except Exception as e:
        st.error(f"Error Loading Document: {str(e)}")
        return []
    
def process_documents(uploaded_files, status_text, progress_bar):
    all_documents = []
    
    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name


            try:
                file_ext = uploaded_file.name.split('.')[-1].lower()
                docs = load_document(tmp_file_path, file_ext)

                if docs:
                    for doc in docs:
                        doc.metadata["source"] = uploaded_file.name
                    
                    all_documents.extend(docs)
                    st.session_state.processed_files.append(uploaded_file.name)

            finally:
                os.unlink(tmp_file_path)
            progress_bar.progress((idx + 1) / len(uploaded_files))

        if not all_documents:
            status_text.text("No documents loaded successfully.")
        return all_documents
    
    status_text.text("Splitting documents into chunks...")


