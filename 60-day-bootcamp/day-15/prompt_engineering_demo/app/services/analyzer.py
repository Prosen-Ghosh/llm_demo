from app.models.schemas import QueryComplexity, PromptStrategy
import re


class QueryAnalyzer:
    """Analyzes query complexity to select optimal prompting strategy"""
    
    # Keywords that indicate complexity
    COMPLEX_KEYWORDS = {
        "explain", "why", "how", "analyze", "compare", 
        "evaluate", "research", "investigate"
    }
    
    MATH_KEYWORDS = {
        "calculate", "solve", "compute", "equation",
        "math", "algebra", "sum", "multiply"
    }
    
    def analyze_complexity(self, query: str) -> QueryComplexity:
        """Determine query complexity using heuristics"""
        query_lower = query.lower()
        word_count = len(query.split())
        
        # Simple queries: < 10 words, no complex keywords
        if word_count < 10 and not any(kw in query_lower for kw in self.COMPLEX_KEYWORDS):
            return QueryComplexity.SIMPLE
        
        # Complex queries: > 20 words OR multiple clauses
        if word_count > 20 or query.count("?") > 1 or query.count(",") > 2:
            return QueryComplexity.COMPLEX
        
        # Medium complexity
        return QueryComplexity.MEDIUM
    
    def suggest_strategy(self, query: str) -> PromptStrategy:
        """Suggest the best prompting strategy based on query analysis"""
        query_lower = query.lower()
        
        # Math problems → Self-Consistency for accuracy
        if any(kw in query_lower for kw in self.MATH_KEYWORDS):
            return PromptStrategy.SELF_CONSISTENCY
        
        # Research/multi-step → ReAct
        if any(kw in query_lower for kw in ["research", "find", "investigate", "steps"]):
            return PromptStrategy.REACT
        
        # Reasoning problems → Chain-of-Thought
        if any(kw in query_lower for kw in ["explain", "why", "analyze"]):
            return PromptStrategy.CHAIN_OF_THOUGHT
        
        # Default
        complexity = self.analyze_complexity(query)
        if complexity == QueryComplexity.SIMPLE:
            return PromptStrategy.DIRECT
        return PromptStrategy.CHAIN_OF_THOUGHT