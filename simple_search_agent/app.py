import os
import streamlit as st
from dotenv import load_dotenv
from utils import init_session
from agent_tools import create_agent, web_search


load_dotenv()
init_session()

st.set_page_config(page_title="Simple Search Agent Demo", layout="wide")
st.title("🔍 Simple Search Agent (LangChain + SerpAPI)")

st.sidebar.header("🔧 LLM Configuration")
st.sidebar.markdown("---")

# API Key input
llm_api_key = st.sidebar.text_input(
    "Enter your OpenRouter API Key:",
    type="password",
    value=st.session_state.llm_api_key or "",
    placeholder="sk-or-v1-...",
    help="Enter your API key from OpenRouter (https://openrouter.ai/keys)"
)

if llm_api_key:
    st.session_state.llm_api_key = llm_api_key
    st.sidebar.success("✅ API key saved for this session")
else:
    st.sidebar.warning("⚠️ Please enter your OpenRouter API key")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Get your API key from [OpenRouter](https://openrouter.ai/keys)")

# Model selection
model_options = [
    "openai/gpt-3.5-turbo",  # Most affordable
    "meta-llama/llama-3.1-8b-instruct",  # Very cheap
    "google/gemini-flash-1.5",  # Fast and cheap
    "deepseek/deepseek-r1-0528",  # More expensive
    "anthropic/claude-3.5-sonnet",  # Premium
    "openai/gpt-4-turbo",  # Premium
]
selected_model = st.sidebar.selectbox(
    "Select Model:",
    model_options,
    index=3,
    help="Choose the AI model (ordered by cost, cheapest first)"
)
os.environ['OPENAI_MODEL'] = selected_model

st.sidebar.markdown("---")
# Main interface
st.markdown("### Ask a question about current events")

query = st.text_input(
    "Your question:",
    placeholder="What's new about the Mars mission?",
    help="Ask about recent events, news, or any topic that requires web search"
)

num_results = st.slider(
    "Number of search results to use:",
    min_value=1,
    max_value=3,
    value=1,  # Reduced default to save tokens
    help="More results provide more context but use more tokens and cost more"
)

col1, col2 = st.columns([1, 4])
with col1:
    ask_button = st.button("🚀 Ask", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

if clear_button:
    st.rerun()

if ask_button:
    if not query.strip():
        st.warning("⚠️ Please enter a question.")
    elif not llm_api_key:
        st.error("❌ Please enter your OpenRouter API key in the sidebar.")
    else:
        tab1, tab2 = st.tabs(["🤖 Agent Answer", "🔍 Search Results"])
        
        answer = None
        snippets = None
        
        with tab1:
            with st.spinner("🤔 Agent is thinking..."):
                try:
                    agent = create_agent(llm_api_key)
                    result = agent.invoke({"input": query, num_results: num_results}, tools={"web_search": web_search})
                    
                    answer = result.get("output", "No answer generated")
                    
                    st.markdown("### Agent's Response")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ Error running agent: {str(e)}")
                    st.exception(e)
                    answer = None
        
        with tab2:
            with st.spinner("🌐 Fetching search results..."):
                try:
                    snippets = web_search.invoke({"query": query, "num_results": num_results})
                    
                    st.markdown("### Raw Search Snippets")
                    st.text_area(
                        "Search results:",
                        snippets,
                        height=400,
                        disabled=True
                    )
                except Exception as e:
                    st.error(f"❌ Error fetching search results: {str(e)}")
                    st.exception(e)
                    snippets = None
        
# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
    Built with LangChain, OpenRouter, and SerpAPI | 
    <a href='https://openrouter.ai' target='_blank'>Get OpenRouter API</a> | 
    <a href='https://serpapi.com' target='_blank'>Get SerpAPI Key</a>
    </div>
    """,
    unsafe_allow_html=True
)