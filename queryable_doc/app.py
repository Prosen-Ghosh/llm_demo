import streamlit as st
from utils import init_session
from ui.sidebar_config import render_sidebar
from ui.footer import render_footer
from ui.main import render_body_content

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide"
)

init_session()
print(f'Streamlit Session: {st.session_state}')

st.title("📚 RAG Document Q&A System")
st.markdown("Upload documents (PDF, DOC, DOCX, TXT) and ask questions about their content!")

render_sidebar()
render_body_content()
render_footer()