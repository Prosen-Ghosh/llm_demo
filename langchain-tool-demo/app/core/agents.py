from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from app.core.config import settings
from app.core.tools import TOOLS

class AgentManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.llm = ChatOllama(
            model=settings.ollama_model,
            temperature=0,
            base_url=settings.ollama_base_url,
        )
        
        self.agent = create_agent(
            model=self.llm,
            tools=TOOLS,
            system_prompt="You are a helpful shopping assistant."
        )
    
    def get_agent(self):
        return self.agent

# Singleton instance
agent_manager = AgentManager()