import logging
from app.jobs import job_manager, JobStatus
from app.whisper import whisper_service
from app.preprocessing import normalize_audio
from app.utils import delete_file
from app.caching import results_cache, compute_file_hash

logger = logging.getLogger("whisper-api")

def process_transcription_job(
        job_id: str, 
        file_path: str, 
        language: str, 
        beam_size: int = 5, 
        best_of: int = 5, 
        initial_prompt: str = None
    ):
    logger.info(f"Starting job {job_id} for file {file_path}")
    job_manager.update_status(job_id, JobStatus.PROCESSING)
    
    processed_path = None
    
    try:
        file_hash = compute_file_hash(file_path)
        cached_result = results_cache.get(f"{file_hash}_{language}")
        
        if cached_result:
            cached_result["cached"] = True
            job_manager.update_status(job_id, JobStatus.COMPLETED, result=cached_result)
            return
        
        processed_path = normalize_audio(file_path)
        result = whisper_service.transcribe_file(
            processed_path, 
            language=language,
            beam_size=beam_size,
            best_of=best_of,
            initial_prompt=initial_prompt
        )
        
        output = {
            "text": result["text"],
            "language": result["language"],
            "duration": result["duration"],
            "segments": result["segments"],
            "model": result["model_used"],
            "cached": False
        }
        results_cache.put(f"{file_hash}_{language}", output)
        
        job_manager.update_status(job_id, JobStatus.COMPLETED, result=output)
        logger.info(f"Job {job_id} completed successfully.")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        job_manager.update_status(job_id, JobStatus.FAILED, error=str(e))
        
    finally:
        delete_file(file_path)
        if processed_path:
            delete_file(processed_path)