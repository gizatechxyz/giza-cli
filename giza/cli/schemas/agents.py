import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, RootModel


class Agent(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Dict[str, Any] = {}
    created_date: Optional[datetime.datetime] = None
    last_update: Optional[datetime.datetime] = None


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class AgentCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Dict[str, Any] = {}


class AgentList(RootModel):
    root: list[Agent]
