import asyncio
import time
from typing import Any, Dict, List
from tenacity import retry, stop_after_attempt, wait_exponential
from app.tools.registry import tool_registry
from app.models.schemas import ToolResult, ToolStatus
from app.core.config import settings
from app.utils.logger import logger


class ToolExecutor:
    @staticmethod
    @retry(
        stop=stop_after_attempt(settings.max_tool_retries),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def execute_with_retry(tool_name: str, **kwargs: Any) -> Any:
        tool = tool_registry.get_tool(tool_name)
        
        # Validate parameters against schema
        validated_params = tool.parameters_schema(**kwargs)
        
        # Execute with timeout
        try:
            result = await asyncio.wait_for(
                tool.execute(**validated_params.model_dump()),
                timeout=settings.tool_timeout_seconds
            )
            return result
        except asyncio.TimeoutError:
            raise TimeoutError(f"Tool '{tool_name}' exceeded timeout of {settings.tool_timeout_seconds}s")
    
    @staticmethod
    async def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> ToolResult:
        start_time = time.time()
        
        try:
            result = await ToolExecutor.execute_with_retry(tool_name, **arguments)
            execution_time = (time.time() - start_time) * 1000
            
            logger.info(
                "tool_executed",
                tool_name=tool_name,
                arguments=arguments,
                result=result,
                execution_time_ms=execution_time,
                status="success"
            )
            
            return ToolResult(
                tool_name=tool_name,
                status=ToolStatus.SUCCESS,
                result=result,
                execution_time_ms=execution_time
            )
            
        except TimeoutError as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(
                "tool_timeout",
                tool_name=tool_name,
                arguments=arguments,
                error=str(e),
                execution_time_ms=execution_time
            )
            
            return ToolResult(
                tool_name=tool_name,
                status=ToolStatus.TIMEOUT,
                error=str(e),
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(
                "tool_failed",
                tool_name=tool_name,
                arguments=arguments,
                error=str(e),
                execution_time_ms=execution_time
            )
            
            return ToolResult(
                tool_name=tool_name,
                status=ToolStatus.FAILED,
                error=str(e),
                execution_time_ms=execution_time
            )
    
    @staticmethod
    async def execute_parallel(tool_calls: List[Dict[str, Any]]) -> List[ToolResult]:
        tasks = [
            ToolExecutor.execute_tool(call["name"], call["arguments"])
            for call in tool_calls
        ]
        return await asyncio.gather(*tasks)