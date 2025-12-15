from app.models.schemas import QueryComplexity, PromptStrategy
import re


class QueryAnalyzer:
    COMPLEX_KEYWORDS = {
        "explain", "why", "how", "analyze", "compare", 
        "evaluate", "research", "investigate"
    }
    
    MATH_KEYWORDS = {
        "calculate", "solve", "compute", "equation",
        "math", "algebra", "sum", "multiply"
    }
    
    def analyze_complexity(self, query: str) -> QueryComplexity:
        query_lower = query.lower()
        word_count = len(query.split())
        
        if word_count < 10 and not any(kw in query_lower for kw in self.COMPLEX_KEYWORDS):
            return QueryComplexity.SIMPLE
        
        if word_count > 20 or query.count("?") > 1 or query.count(",") > 2:
            return QueryComplexity.COMPLEX
        
        return QueryComplexity.MEDIUM
    
    def suggest_strategy(self, query: str) -> PromptStrategy:
        query_lower = query.lower()
        
        if any(kw in query_lower for kw in self.MATH_KEYWORDS):
            return PromptStrategy.SELF_CONSISTENCY
        
        if any(kw in query_lower for kw in ["research", "find", "investigate", "steps"]):
            return PromptStrategy.REACT
        
        if any(kw in query_lower for kw in ["explain", "why", "analyze"]):
            return PromptStrategy.CHAIN_OF_THOUGHT
        
        # Default
        complexity = self.analyze_complexity(query)
        if complexity == QueryComplexity.SIMPLE:
            return PromptStrategy.DIRECT
        return PromptStrategy.CHAIN_OF_THOUGHT