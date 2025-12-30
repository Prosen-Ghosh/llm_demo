from fastapi import FastAPI, Request, UploadFile, File, HTTPException, BackgroundTasks, Query
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
from app.utils import validate_file_extension, save_upload_file_tmp, delete_file, check_model_suitability
from app.preprocessing import normalize_audio
from app.jobs import job_manager, Job
from app.worker import process_transcription_job
from typing import List

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
        model_size=settings.DEFAULT_MODEL_SIZE,
        cpu_threads=multiprocessing.cpu_count()
    )

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} v{settings.VERSION}"}

@app.post("/transcribe")
def transcribe_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    language: str = Query("en", min_length=2, max_length=2, description="Language code (e.g., en, es, bn)")
):
    validate_file_extension(file.filename)
    temp_file_path = save_upload_file_tmp(file)
    processed_file_path = None
    try:
        processed_file_path = normalize_audio(temp_file_path)
        current_model = whisper_service.current_model_size
        suitability_warning = check_model_suitability(language, current_model)

        logger.info(f"Processing file: {file.filename} ({processed_file_path})")
        result = whisper_service.transcribe_file(processed_file_path, language=language)
        
        response_payload = {
            "filename": file.filename,
            "model": result["model_used"],
            "language": result["language"],
            "duration": result["duration"],
            "language_probability": result["language_probability"],
            "text": result["text"],
            "segments": result["segments"]
        }

        if suitability_warning:
            response_payload["system_warning"] = suitability_warning

        return response_payload

    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        background_tasks.add_task(delete_file, temp_file_path)
        if processed_file_path:
            background_tasks.add_task(delete_file, processed_file_path)


@app.put("/system/model")
def switch_model(model_size: str):
    if model_size not in settings.ALLOWED_MODELS:
        raise HTTPException(status_code=400, detail=f"Model not allowed. Options: {settings.ALLOWED_MODELS}")
    
    try:
        whisper_service.load_model(model_size)
        return {"status": "success", "current_model": model_size}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/v2/batch-transcribe", response_model=List[str])
def batch_transcribe(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    language: str = Query("en", min_length=2, max_length=2)
):
    job_ids = []
    
    for file in files:
        validate_file_extension(file.filename)
        file_path = save_upload_file_tmp(file)
        job_id = job_manager.create_job(file.filename)
        job_ids.append(job_id)

        background_tasks.add_task(
            process_transcription_job, 
            job_id, 
            file_path, 
            language
        )
        
    return job_ids

@app.get("/v2/jobs/{job_id}", response_model=Job)
def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job