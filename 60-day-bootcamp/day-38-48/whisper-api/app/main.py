from fastapi import FastAPI, Request, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import logging
import time
import os
import wave
import struct
from app.config import settings
from app.whisper import whisper_service
from app.utils import validate_file_extension, save_upload_file_tmp, delete_file

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("whisper-api")

def create_test_audio(filename="test_audio.wav"):
    if os.path.exists(filename):
        return
    with wave.open(filename, 'w') as f:
        f.setparams((1, 2, 44100, 44100, 'NONE', 'not compressed'))
        for _ in range(44100):
            value = struct.pack('<h', 0)
            f.writeframes(value)
    logger.info(f"Created dummy test audio: {filename}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Whisper Service...")
    whisper_service.load_model()
    # create_test_audio("test_audio.wav")
    
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    description="High-performance CPU-based Speech-to-Text API",
)

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    cpu_cores_available: int
    model_loaded: bool
    model_size: str
    cpu_threads: int

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
        cpu_cores_available=multiprocessing.cpu_count(),
        model_loaded=whisper_service.model is not None,
        model_size=settings.WHISPER_MODEL_SIZE,
        cpu_threads=multiprocessing.cpu_count()
    )

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} v{settings.VERSION}"}

@app.post("/transcribe")
def transcribe_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    validate_file_extension(file.filename)
    temp_file_path = save_upload_file_tmp(file)
    try:
        logger.info(f"Processing file: {file.filename} ({temp_file_path})")
        result = whisper_service.transcribe_file(temp_file_path)
        
        return {
            "filename": file.filename,
            "language": result["language"],
            "duration": result["duration"],
            "text": result["text"],
            "segments": result["segments"] 
        }

    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        background_tasks.add_task(delete_file, temp_file_path)


@app.post("/test-transcribe")
async def test_transcribe():
    try:
        start = time.time()
        result = whisper_service.transcribe_file("test_audio.wav")
        process_time = time.time() - start
        
        return {
            "status": "success",
            "processing_time": round(process_time, 3),
            "result": result
        }
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})