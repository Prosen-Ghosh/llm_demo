from fastapi import FastAPI, Request, UploadFile, File, HTTPException, BackgroundTasks, Query
from fastapi.responses import JSONResponse, StreamingResponse
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
from enum import Enum
import asyncio
from app.monitoring import get_system_metrics, run_garbage_collector
import json

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("whisper-api")

async def periodic_maintenance():
    while True:
        await asyncio.sleep(60)
        run_garbage_collector(max_job_age_seconds=3600)
        
        metrics = get_system_metrics()
        logger.info(f"System Health: RAM={metrics['memory_used_mb']}MB | Jobs={metrics['total_jobs_in_memory']}")

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
    asyncio.create_task(periodic_maintenance())
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

class ProcessingMode(str, Enum):
    ACCURATE = "accurate"  # Beam size 5 (Default)
    BALANCED = "balanced"  # Beam size 2
    TURBO = "turbo"        # Greedy decoding (Beam size 1)

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
    language: str = Query("auto", description="Language code or 'auto'"),
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
    language: str = Query("auto", description="Language code or 'auto'"),
    mode: ProcessingMode = Query(ProcessingMode.ACCURATE, description="Optimization mode"),
    keywords: str = Query(None, description="Comma-separated custom terms (e.g., 'Jashore, Docker, API')")
):
    initial_prompt = None
    if keywords:
        initial_prompt = f"Glossary: {keywords}."

    decode_options = {
        ProcessingMode.ACCURATE: {"beam_size": 5, "best_of": 5},
        ProcessingMode.BALANCED: {"beam_size": 2, "best_of": 2},
        ProcessingMode.TURBO:    {"beam_size": 1, "best_of": 1} # Greedy
    }
    
    params = decode_options[mode]
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
            language,
            params["beam_size"],
            params["best_of"],
            initial_prompt
        )
        
    return job_ids

@app.get("/v2/jobs/{job_id}", response_model=Job)
def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/system/stats")
def system_stats():
    return get_system_metrics()

@app.post("/stream")
async def stream_transcription(
    file: UploadFile = File(...),
    language: str = Query("en", min_length=2, max_length=2),
):
    validate_file_extension(file.filename)
    temp_file_path = save_upload_file_tmp(file)

    def iterfile():
        try:
            processed_path = normalize_audio(temp_file_path)
            yield from whisper_service.stream_transcribe(processed_path, language=language)
            delete_file(processed_path)
            
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            delete_file(temp_file_path)

    return StreamingResponse(iterfile(), media_type="text/event-stream")