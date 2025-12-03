from typing import Dict, List, Type
from app.tools.base import BaseTool
from app.tools.calculator import CalculatorTool
from app.tools.weather import WeatherTool
from app.tools.web_search import WebSearchTool
from app.utils.logger import logger


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._auto_register_tools()
    
    def _auto_register_tools(self):
        tool_classes: List[Type[BaseTool]] = [
            CalculatorTool,
            WeatherTool,
            WebSearchTool
        ]
        
        for tool_class in tool_classes:
            tool = tool_class()
            self.register(tool)
            logger.info(
                "tool_registered",
                tool_name=tool.name,
                description=tool.description
            )
    
    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
    
    def get_tool(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found in registry")
        return self._tools[name]
    
    def get_all_tools(self) -> List[BaseTool]:
        return list(self._tools.values())
    
    def get_ollama_schemas(self) -> List[dict]:
        return [tool.to_ollama_schema() for tool in self._tools.values()]

# Global registry instance
tool_registry = ToolRegistry()