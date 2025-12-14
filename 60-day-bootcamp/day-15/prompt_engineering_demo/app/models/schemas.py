from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class PromptStrategy(str, Enum):
    CHAIN_OF_THOUGHT = "chain_of_thought"
    REACT = "react"
    SELF_CONSISTENCY = "self_consistency"
    DIRECT = "direct"


class QueryComplexity(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=2000)
    strategy: Optional[PromptStrategy] = None  # Auto-select if None
    prompt_version: Optional[str] = "latest"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    stream: bool = False
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


class ReasoningStep(BaseModel):
    step_number: int
    thought: str
    action: Optional[str] = None
    observation: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class QueryResponse(BaseModel):
    query: str
    answer: str
    strategy_used: PromptStrategy
    prompt_version: str
    complexity: QueryComplexity
    reasoning_steps: List[ReasoningStep] = []
    metadata: Dict[str, Any] = Field(default_factory=dict)
    token_usage: Dict[str, int] = Field(default_factory=dict)
    latency_ms: float


class PromptVersion(BaseModel):
    version: str  # Semantic versioning: v1.0.0
    name: str
    system_prompt: str
    strategy: PromptStrategy
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = "system"
    changelog: Optional[str] = None
    is_active: bool = True
    performance_metrics: Dict[str, float] = Field(default_factory=dict)


class PromptComparisonRequest(BaseModel):
    version_a: str
    version_b: str
    test_queries: List[str] = Field(..., min_length=1, max_length=10)
    
    
class ComparisonResult(BaseModel):
    version: str
    avg_latency_ms: float
    avg_tokens: int
    responses: List[str]