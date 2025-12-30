from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
import time

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Job(BaseModel):
    id: str
    filename: str
    status: JobStatus
    created_at: float
    completed_at: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class JobManager:
    _instance = None
    _jobs: Dict[str, Job] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JobManager, cls).__new__(cls)
        return cls._instance

    def create_job(self, filename: str) -> str:
        job_id = str(uuid.uuid4())
        self._jobs[job_id] = Job(
            id=job_id,
            filename=filename,
            status=JobStatus.QUEUED,
            created_at=time.time()
        )
        return job_id

    def get_job(self, job_id: str) -> Optional[Job]:
        return self._jobs.get(job_id)

    def update_status(self, job_id: str, status: JobStatus, result=None, error=None):
        if job_id in self._jobs:
            job = self._jobs[job_id]
            job.status = status
            if result:
                job.result = result
                job.completed_at = time.time()
            if error:
                job.error = error
                job.completed_at = time.time()

job_manager = JobManager()