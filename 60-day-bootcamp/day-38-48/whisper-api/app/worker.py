import logging
from app.jobs import job_manager, JobStatus
from app.whisper import whisper_service
from app.preprocessing import normalize_audio
from app.utils import delete_file

logger = logging.getLogger("whisper-api")

def process_transcription_job(job_id: str, file_path: str, language: str):
    logger.info(f"Starting job {job_id} for file {file_path}")
    job_manager.update_status(job_id, JobStatus.PROCESSING)
    
    processed_path = None
    
    try:
        processed_path = normalize_audio(file_path)
        result = whisper_service.transcribe_file(processed_path, language=language)
        
        output = {
            "text": result["text"],
            "language": result["language"],
            "duration": result["duration"],
            "segments": result["segments"],
            "model": result["model_used"]
        }
        job_manager.update_status(job_id, JobStatus.COMPLETED, result=output)
        logger.info(f"Job {job_id} completed successfully.")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        job_manager.update_status(job_id, JobStatus.FAILED, error=str(e))
        
    finally:
        delete_file(file_path)
        if processed_path:
            delete_file(processed_path)