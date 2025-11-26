import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def split_doc_into_chunk(all_documents, chunk_size: int, chunk_overlap: int):
    status_text = st.empty()
    status_text.text("Splitting documents into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    if all_documents:
        chunks = text_splitter.split_documents(all_documents)
        return chunks
    
    return []

def embedding_and_store(chunks, api_key: str):
    status_text = st.empty()
    status_text.text(f"Creating embeddings for {len(chunks)} chunks...")

    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=st.session_state.chroma_dir,
        collection_name="rag_documents"
    )
    
    return vector_store

