from typing import AsyncGenerator, Dict, Any
from app.strategies.base import PromptStrategy


class ChainOfThoughtStrategy(PromptStrategy):
    """
    Chain-of-Thought prompting forces step-by-step reasoning.
    Best for: Math, logic, multi-step problems.
    """
    
    COT_TEMPLATE = """You are a helpful AI assistant. When answering questions, think step-by-step.

Format your response as:
**Reasoning:**
[Your step-by-step thinking process]

**Answer:**
[Your final answer]

Now, answer the following query:"""
    
    async def execute(
        self, 
        query: str, 
        system_prompt: str,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        enhanced_prompt = f"{system_prompt}\n\n{self.COT_TEMPLATE}\n{query}"
        
        response = await self.llm_client.generate(
            prompt=enhanced_prompt,
            temperature=temperature
        )
        
        # Parse reasoning steps
        if "**Reasoning:**" in response["content"]:
            parts = response["content"].split("**Answer:**")
            reasoning = parts[0].replace("**Reasoning:**", "").strip()
            answer = parts[1].strip() if len(parts) > 1 else response["content"]
            
            # Log the reasoning as a step
            self.add_reasoning_step(thought=reasoning)
        else:
            answer = response["content"]
        
        return {
            "answer": answer,
            "reasoning_steps": self.reasoning_steps,
            "token_usage": response.get("token_usage", {})
        }
    
    async def execute_stream(
        self,
        query: str,
        system_prompt: str,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        enhanced_prompt = f"{system_prompt}\n\n{self.COT_TEMPLATE}\n{query}"
        
        async for chunk in self.llm_client.generate_stream(
            prompt=enhanced_prompt,
            temperature=temperature
        ):
            yield chunk