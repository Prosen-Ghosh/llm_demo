import asyncio
from typing import AsyncGenerator, Dict, Any, List
from collections import Counter
from app.strategies.base import PromptStrategy


class SelfConsistencyStrategy(PromptStrategy):
    """
    Self-Consistency: Generate multiple reasoning paths and pick the most common answer.
    Best for: Math problems, objective questions with clear answers.
    
    Cost: 3-5x more tokens than single inference.
    """
    
    NUM_SAMPLES = 3  # Production systems use 5-10
    
    async def execute(
        self, 
        query: str, 
        system_prompt: str,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        # Generate multiple independent responses with high temperature
        tasks = [
            self.llm_client.generate(
                prompt=f"{system_prompt}\n\nQuery: {query}\n\nProvide your answer:",
                temperature=temperature + 0.2  # Increase diversity
            )
            for _ in range(self.NUM_SAMPLES)
        ]
        
        responses = await asyncio.gather(*tasks)
        
        # Extract answers and find consensus
        answers = [r["content"].strip() for r in responses]
        
        # Log each reasoning path
        for i, answer in enumerate(answers, 1):
            self.add_reasoning_step(
                thought=f"Sample {i}: {answer[:100]}...",
                action="generate_sample"
            )
        
        # Find most common answer (simple majority voting)
        answer_counter = Counter(answers)
        most_common_answer, count = answer_counter.most_common(1)[0]
        
        self.add_reasoning_step(
            thought=f"Consensus reached: {count}/{self.NUM_SAMPLES} samples agree",
            action="majority_vote",
            observation=most_common_answer
        )
        
        # Aggregate token usage
        total_tokens = sum(r.get("token_usage", {}).get("total_tokens", 0) for r in responses)
        
        return {
            "answer": most_common_answer,
            "reasoning_steps": self.reasoning_steps,
            "token_usage": {"total_tokens": total_tokens},
            "metadata": {
                "all_answers": answers,
                "consensus_strength": count / self.NUM_SAMPLES
            }
        }
    
    async def execute_stream(
        self,
        query: str,
        system_prompt: str,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        # Self-consistency doesn't stream well (needs all samples first)
        result = await self.execute(query, system_prompt, temperature)
        yield result["answer"]