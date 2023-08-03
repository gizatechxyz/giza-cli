import datetime
from typing import Optional

from pydantic import BaseModel

from giza.utils.enums import JobSize, JobStatus


class Job(BaseModel):
    id: int
    job_name: Optional[str] = None
    size: str
    status: JobStatus
    elapsed_time: Optional[float] = None
    created_date: Optional[datetime.datetime] = None
    last_update: Optional[datetime.datetime] = None


class JobCreate(BaseModel):
    size: JobSize
