import datetime
from typing import Optional

from pydantic import BaseModel, RootModel


class Proof(BaseModel):
    id: int
    job_id: int
    proving_time: Optional[float] = None
    cairo_execution_time: Optional[float] = None
    metrics: Optional[dict] = None
    created_date: datetime.datetime
    request_id: Optional[str] = None


class ProofList(RootModel):
    root: list[Proof]
