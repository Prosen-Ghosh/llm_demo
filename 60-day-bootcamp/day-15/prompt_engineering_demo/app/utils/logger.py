import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class StructuredLogger:
    """Structured JSON logger for reasoning traces and costs"""
    
    def __init__(self, log_file: str = "logs/reasoning_traces.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
    
    def log_query(
        self,
        query: str,
        response: str,
        strategy: str,
        complexity: str,
        token_usage: Dict[str, int],
        latency_ms: float,
        reasoning_steps: list
    ):
        """Log structured query data"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "response": response[:200],  # Truncate for storage
            "strategy": strategy,
            "complexity": complexity,
            "token_usage": token_usage,
            "latency_ms": latency_ms,
            "num_reasoning_steps": len(reasoning_steps),
            "cost_estimate_usd": self._estimate_cost(token_usage)
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def _estimate_cost(self, token_usage: Dict[str, int]) -> float:
        """Estimate cost based on Ollama (free) or OpenRouter pricing"""
        # Ollama is free, but we track opportunity cost
        # OpenRouter: ~$0.001 per 1K tokens for free models
        total_tokens = token_usage.get("total_tokens", 0)
        return (total_tokens / 1000) * 0.001