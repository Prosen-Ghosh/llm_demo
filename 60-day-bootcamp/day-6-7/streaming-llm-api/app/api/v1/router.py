from fastapi import APIRouter
from app.api.v1.endpoints import chat, health, usage

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])