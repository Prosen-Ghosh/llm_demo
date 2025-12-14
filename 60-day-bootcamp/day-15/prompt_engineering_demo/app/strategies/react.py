from typing import AsyncGenerator, Dict, Any
from app.strategies.base import PromptStrategy


class ReActStrategy(PromptStrategy):
    """
    ReAct (Reasoning + Acting) prompting for tool-using agents.
    Best for: Research tasks, multi-step queries requiring external tools.
    
    Format: Thought -> Action -> Observation -> ... -> Answer
    """
    
    REACT_TEMPLATE = """You are an AI assistant that uses the ReAct framework.

Answer the query using this format:
Thought: [Your reasoning about what to do next]
Action: [What action you would take, e.g., "Search", "Calculate", "Verify"]
Observation: [What you would expect to observe from that action]

Repeat Thought/Action/Observation as needed, then provide:
Answer: [Your final answer]

Query:"""
    
    MAX_ITERATIONS = 3  # Prevent infinite loops
    
    async def execute(
        self, 
        query: str, 
        system_prompt: str,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        enhanced_prompt = f"{system_prompt}\n\n{self.REACT_TEMPLATE}\n{query}"
        
        response = await self.llm_client.generate(
            prompt=enhanced_prompt,
            temperature=temperature
        )
        
        # Parse ReAct steps
        content = response["content"]
        steps = self._parse_react_steps(content)
        
        for step in steps:
            self.add_reasoning_step(
                thought=step.get("thought", ""),
                action=step.get("action"),
                observation=step.get("observation")
            )
        
        # Extract final answer
        answer = self._extract_answer(content)
        
        return {
            "answer": answer,
            "reasoning_steps": self.reasoning_steps,
            "token_usage": response.get("token_usage", {})
        }
    
    def _parse_react_steps(self, content: str) -> list[Dict[str, str]]:
        """Parse ReAct formatted response into structured steps"""
        steps = []
        lines = content.split("\n")
        current_step = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith("Thought:"):
                if current_step:
                    steps.append(current_step)
                current_step = {"thought": line.replace("Thought:", "").strip()}
            elif line.startswith("Action:"):
                current_step["action"] = line.replace("Action:", "").strip()
            elif line.startswith("Observation:"):
                current_step["observation"] = line.replace("Observation:", "").strip()
        
        if current_step:
            steps.append(current_step)
        
        return steps
    
    def _extract_answer(self, content: str) -> str:
        """Extract final answer from ReAct output"""
        if "Answer:" in content:
            return content.split("Answer:")[-1].strip()
        return content
    
    async def execute_stream(
        self,
        query: str,
        system_prompt: str,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        enhanced_prompt = f"{system_prompt}\n\n{self.REACT_TEMPLATE}\n{query}"
        
        async for chunk in self.llm_client.generate_stream(
            prompt=enhanced_prompt,
            temperature=temperature
        ):
            yield chunk