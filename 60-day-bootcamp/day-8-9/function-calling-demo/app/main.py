from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health_router, chat_router, tools_router

app = FastAPI(
    title="Function Calling Demo",
    description="Enterprise-grade function calling system with OpenRouter",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=['health'])
app.include_router(chat_router, tags=['chat'])
app.include_router(tools_router, tags=['tools'])