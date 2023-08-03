from typing import Optional

from pydantic import BaseModel

from giza.utils.enums import ModelStatus


class Model(BaseModel):
    id: int
    size: int
    name: Optional[str] = None
    status: Optional[ModelStatus] = None
    message: Optional[str] = None


class ModelCreate(BaseModel):
    size: int
    name: str
    status: ModelStatus = ModelStatus.STARTING
    message: Optional[str] = None


class ModelUpdate(BaseModel):
    status: ModelStatus
