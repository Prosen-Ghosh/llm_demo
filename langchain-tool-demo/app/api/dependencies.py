from fastapi import Depends
from app.core.agents import agent_manager

def get_agent():
    return agent_manager.get_agent()