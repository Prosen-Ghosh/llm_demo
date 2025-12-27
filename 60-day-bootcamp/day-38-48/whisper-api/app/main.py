from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import time
from app.config import settings

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("whisper-api")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="High-performance CPU-based Speech-to-Text API",
)

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    cpu_cores_available: int

start_time = time.time()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    logger.info(
        f"Path: {request.url.path} | Method: {request.method} | "
        f"Status: {response.status_code} | Duration: {process_time:.4f}s"
    )
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    import multiprocessing
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        uptime_seconds=round(time.time() - start_time, 2),
        cpu_cores_available=multiprocessing.cpu_count()
    )

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} v{settings.VERSION}"}