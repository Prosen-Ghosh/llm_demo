from fastapi import APIRouter
from app.tools.registry import tool_registry

router = APIRouter()

@router.get("/tools")
async def list_tools():
    tools = tool_registry.get_all_tools()
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema.model_json_schema()
            }
            for tool in tools
        ]
    }
