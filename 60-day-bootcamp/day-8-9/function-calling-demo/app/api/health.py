from fastapi import APIRouter
from app.tools.registry import tool_registry
router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy", "tools_registered": len(tool_registry.get_all_tools())}

