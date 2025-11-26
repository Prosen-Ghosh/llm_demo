from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import streamlit as st

def get_chat_response(query: str, vector_store):
    openai_api_key=st.session_state.openai_api_key
    temperature = float(st.session_state.temperature)
    top_k = int(st.session_state.top_k)
    model = st.session_state.llm_model

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )

    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key=openai_api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8501",  # Optional: Your app URL
            "X-Title": "RAG Document Q&A"  # Optional: Your app name
        }
    )

    system_prompt = """You are a helpful assistant that answers questions based on the provided context.

Instructions:
- Answer the question using ONLY the information from the provided context
- If the context doesn't contain relevant information, say "I don't have enough information in the provided documents to answer that question."
- Be concise but comprehensive
- Cite the source document when possible

Context:
{context}"""

    prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    response = rag_chain.invoke({"input": query})
    
    return response


def display_chat():
    if st.session_state.chat_history:
        st.divider()
    st.header("💭 Chat History")
    
    for idx, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"Q: {chat['question'][:100]}...", expanded=(idx == 0)):
            st.markdown("**Question:**")
            st.write(chat["question"])
            
            st.markdown("**Answer:**")
            st.write(chat["answer"])
            
            if chat.get("sources"):
                st.markdown("**Source Chunks:**")
                for i, source in enumerate(chat["sources"][:3], 1):
                    source_name = source.metadata.get("source", "Unknown")
                    st.markdown(f"*Source {i} ({source_name}):*")
                    st.text(source.page_content[:300] + "...")
