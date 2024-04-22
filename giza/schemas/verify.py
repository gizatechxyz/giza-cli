from typing import Optional

from pydantic import BaseModel


class VerifyResponse(BaseModel):
    verification: Optional[bool] = None
    verification_time: Optional[float] = None
