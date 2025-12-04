from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Shopping Assistant API",
    description="AI-powered shopping assistant",
    version="1.0.0"
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Shopping Assistant API"}