from collections import defaultdict
from app.models.usage import UsageStats

class CostTracker:
    def __init__(self):
        # In-memory storage (use Redis in production)
        self.usage_by_key: dict[str, UsageStats] = defaultdict(UsageStats)
    
    def record_usage(
        self,
        api_key: str,
        prompt_tokens: int,
        completion_tokens: int,
        model: str
    ) -> UsageStats:
        stats = self.usage_by_key[api_key]
        
        stats.total_requests += 1
        stats.prompt_tokens += prompt_tokens
        stats.completion_tokens += completion_tokens
        stats.total_tokens += (prompt_tokens + completion_tokens)
        
        # Estimate cost (free models = $0, but we track for monitoring)
        cost_per_1k = 0.0  # Free models
        if ":free" not in model.lower():
            # Rough estimates for paid models
            cost_per_1k = 0.002 if "gpt-4" in model else 0.0005
        
        stats.estimated_cost_usd += (stats.total_tokens / 1000) * cost_per_1k
        
        return stats
    
    def get_usage(self, api_key: str) -> UsageStats:
        return self.usage_by_key.get(api_key, UsageStats())
    
cost_tracker = CostTracker()