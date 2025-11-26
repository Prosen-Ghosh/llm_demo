import streamlit as st

def render_footer():
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Built with Streamlit, LangChain, and OpenRouter | RAG Document Q&A System</p>
    </div>
    """, unsafe_allow_html=True)