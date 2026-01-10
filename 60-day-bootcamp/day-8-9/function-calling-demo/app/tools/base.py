from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any, Type


class BaseTool(ABC):
    name: str
    description: str
    parameters_schema: Type[BaseModel]
    
    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        pass
    
    def to_ollama_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters_schema.model_json_schema()
            }
        }