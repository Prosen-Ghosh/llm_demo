from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, List
from app.models.schemas import ReasoningStep


class PromptStrategy(ABC):
    def __init__(self, llm_client: Any):
        self.llm_client = llm_client
        self.reasoning_steps: List[ReasoningStep] = []
    
    @abstractmethod
    async def execute(
        self, 
        query: str, 
        system_prompt: str,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def execute_stream(
        self,
        query: str,
        system_prompt: str,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        pass
    
    def add_reasoning_step(
        self, 
        thought: str, 
        action: str = None, 
        observation: str = None
    ) -> None:
        step = ReasoningStep(
            step_number=len(self.reasoning_steps) + 1,
            thought=thought,
            action=action,
            observation=observation
        )
        self.reasoning_steps.append(step)