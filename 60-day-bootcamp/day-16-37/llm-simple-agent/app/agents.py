import os
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langchain_core.callbacks import BaseCallbackHandler

llm = ChatOllama(
    model="gpt-oss:120b-cloud", # specify your tools supported model here, e.g., gpt-oss:7b, gpt-oss:13b, gpt-oss:120b-cloud
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0
)

@tool
def calculator(expression: str) -> str:
    """Useful for performing mathematical calculations. 
    Input should be a mathematical expression string like '2 + 2' or '25 * 4'."""
    try:
        return str(eval(expression)) # Warning: eval is dangerous in prod, but ok for a local demo
    except Exception as e:
        return f"Error calculating: {e}"

@tool
def web_search(query: str) -> str:
    """Useful for finding facts, general knowledge, or current events.
    Input should be a search query."""
    return f"I searched the simulated web for '{query}' and found that LangGraph is awesome!"

tools = [calculator, web_search]

agent_executor = create_agent(llm, tools)

def run_agent(user_query: str):
    response = agent_executor.invoke(
        {"messages": [HumanMessage(content=user_query)]},
        {"callbacks": [ConsoleCallbackHandler()]}
    )
    print(f"Full response: {response}")
    return response["messages"][-1].content

class ConsoleCallbackHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"\n🔧 Using tool: {serialized.get('name', serialized)}")
        print(f"Tool input: {input_str}")
    
    def on_tool_end(self, output, **kwargs):
        print(f"Tool output: {output}\n")