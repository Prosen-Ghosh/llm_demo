from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import time
from typing import AsyncGenerator, Optional, List

from app.models.schemas import (
    QueryRequest, QueryResponse, PromptVersion,
    PromptComparisonRequest, ComparisonResult,
    PromptStrategy as PromptStrategyEnum
)
from app.services.llm_client import OllamaClient
from app.config import settings
from app.services.prompt_manager import PromptVersionManager
from app.services.analyzer import QueryAnalyzer
from app.strategies.chain_of_thought import ChainOfThoughtStrategy
from app.strategies.react import ReActStrategy
from app.strategies.self_consistency import SelfConsistencyStrategy
from app.utils.logger import StructuredLogger

llm_client = OllamaClient()
prompt_manager = PromptVersionManager(settings.database_url if hasattr(settings, 'database_url') else "sqlite+aiosqlite:///./data/prompts.db")
query_analyzer = QueryAnalyzer()
structured_logger = StructuredLogger()
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    await prompt_manager.initialize()
    yield
    await llm_client.close()

app = FastAPI(
title="Prompt Engineering Demo",
description="Production-grade prompt orchestration with versioning",
version="1.0.0",
lifespan=lifespan
)
def get_strategy(strategy_type: PromptStrategyEnum):
    """Factory function for strategy selection"""
    strategies = {
        PromptStrategyEnum.CHAIN_OF_THOUGHT: ChainOfThoughtStrategy,
        PromptStrategyEnum.REACT: ReActStrategy,
        PromptStrategyEnum.SELF_CONSISTENCY: SelfConsistencyStrategy,
    }
    strategy_class = strategies.get(strategy_type)
    if not strategy_class:
        raise HTTPException(400, f"Strategy {strategy_type} not implemented")

    return strategy_class(llm_client)
@app.post("/v1/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with auto-strategy selection"""
    start_time = time.time()
    # Analyze query complexity
    complexity = query_analyzer.analyze_complexity(request.query)

    # Select strategy
    if request.strategy:
        strategy_type = request.strategy
    else:
        strategy_type = query_analyzer.suggest_strategy(request.query)

    print(f'strategy_type:: {strategy_type.value}')
    print(f"request.prompt_version => {request.prompt_version}")
    # Get prompt version
    prompt_version = await prompt_manager.get_version(
        request.prompt_version or "v1.0.0",
        strategy_type.value
    )

    if not prompt_version:
        raise HTTPException(404, "Prompt version not found")

    # Execute strategy
    strategy = get_strategy(strategy_type)
    result = await strategy.execute(
        query=request.query,
        system_prompt=prompt_version.system_prompt,
        temperature=request.temperature
    )

    latency_ms = (time.time() - start_time) * 1000

    # Log the query
    structured_logger.log_query(
        query=request.query,
        response=result["answer"],
        strategy=strategy_type.value,
        complexity=complexity.value,
        token_usage=result["token_usage"],
        latency_ms=latency_ms,
        reasoning_steps=result["reasoning_steps"]
    )

    return QueryResponse(
        query=request.query,
        answer=result["answer"],
        strategy_used=strategy_type,
        prompt_version=prompt_version.version,
        complexity=complexity,
        reasoning_steps=result["reasoning_steps"],
        token_usage=result["token_usage"],
        latency_ms=latency_ms,
        metadata=result.get("metadata", {})
    )


@app.post("/v1/query/stream")
async def query_stream_endpoint(request: QueryRequest):
    """Streaming query endpoint"""
    # Similar logic but returns StreamingResponse
    complexity = query_analyzer.analyze_complexity(request.query)
    strategy_type = request.strategy or query_analyzer.suggest_strategy(request.query)
    prompt_version = await prompt_manager.get_version(
        request.prompt_version or "v1.0.0",
        strategy_type.value
    )

    if not prompt_version:
        raise HTTPException(404, "Prompt version not found")

    strategy = get_strategy(strategy_type)

    async def generate() -> AsyncGenerator[str, None]:
        async for chunk in strategy.execute_stream(
            query=request.query,
            system_prompt=prompt_version.system_prompt,
            temperature=request.temperature
        ):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")


@app.post("/v1/prompts/version", response_model=PromptVersion)
async def create_prompt_version(prompt: PromptVersion):
    """Create a new prompt version"""
    return await prompt_manager.create_version(prompt)

@app.get("/v1/prompts/versions")
async def list_prompt_versions(strategy: str = None):
    """List all prompt versions"""
    return await prompt_manager.list_versions(strategy)

@app.post("/v1/prompts/compare")
async def compare_prompts(request: PromptComparisonRequest):
    """A/B test two prompt versions"""
    results = {"version_a": None, "version_b": None}
    for version_id in ["version_a", "version_b"]:
        version = getattr(request, version_id)
        total_latency = 0
        total_tokens = 0
        responses = []
        
        for query in request.test_queries:
            start = time.time()
            # Execute query with this version
            # (Simplified - would need strategy detection)
            strategy = ChainOfThoughtStrategy(llm_client)
            prompt_ver = await prompt_manager.get_version(version, "chain_of_thought")
            
            if not prompt_ver:
                continue
                
            result = await strategy.execute(query, prompt_ver.system_prompt)
            
            total_latency += (time.time() - start) * 1000
            total_tokens += result["token_usage"].get("total_tokens", 0)
            responses.append(result["answer"][:100])
        
        results[version_id] = ComparisonResult(
            version=version,
            avg_latency_ms=total_latency / len(request.test_queries),
            avg_tokens=total_tokens // len(request.test_queries),
            responses=responses
        )

    return results
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": settings.ollama_model}

async def get_prompt_manager() -> PromptVersionManager:
    """Dependency to get prompt manager instance"""
    manager = PromptVersionManager(settings.database_url)
    await manager.initialize()  # Ensure tables are created
    return manager

@app.get("/", response_model=List[PromptVersion])
async def list_prompts(
    strategy: Optional[PromptStrategyEnum] = Query(None, description="Filter by strategy"),
    active_only: bool = Query(True, description="Show only active prompts"),
    prompt_manager: PromptVersionManager = Depends(get_prompt_manager)
):
    """
    Get all prompts from the database
    
    - **strategy**: Filter by prompt strategy (cot, react, direct)
    - **active_only**: Show only active prompts (default: True)
    """
    try:
        # Get all prompts
        prompts = await prompt_manager.list_versions(
            strategy=strategy.value if strategy else None
        )
        
        # Filter active prompts if requested
        if active_only:
            prompts = [p for p in prompts if p.is_active]
        
        return prompts
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching prompts: {str(e)}"
        )