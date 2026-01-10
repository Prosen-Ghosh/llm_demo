import psutil
import os
import time
import logging
from app.jobs import job_manager, JobStatus

logger = logging.getLogger("whisper-api")

def get_system_metrics():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_used_mb": round(mem_info.rss / 1024 / 1024, 2),
        "memory_percent": process.memory_percent(),
        "total_jobs_in_memory": len(job_manager._jobs)
    }

def run_garbage_collector(max_job_age_seconds: int = 3600):
    current_time = time.time()
    jobs_to_delete = []
    
    for job_id, job in job_manager._jobs.items():
        if job.status in [JobStatus.COMPLETED, JobStatus.FAILED]:
            if job.completed_at and (current_time - job.completed_at > max_job_age_seconds):
                jobs_to_delete.append(job_id)
    
    for job_id in jobs_to_delete:
        del job_manager._jobs[job_id]
        
    if jobs_to_delete:
        logger.info(f"Garbage Collector: Removed {len(jobs_to_delete)} old jobs. RAM Freed.")