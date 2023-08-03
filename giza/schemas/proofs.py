import datetime

from pydantic import BaseModel


class Proof(BaseModel):
    id: int
    job_id: int
    proving_time: float
    cairo_execution_time: float
    created_date: datetime.datetime
