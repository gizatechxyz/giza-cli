from typing import Optional

from pydantic import BaseModel

from giza.utils.enums import Framework, ServiceSize


class EndpointCreate(BaseModel):
    file: Optional[str] = None
    uri: Optional[str] = None
    model_id: Optional[int] = None
    version_id: Optional[int] = None
    status: Optional[str] = None
    size: ServiceSize
    service_name: Optional[str] = None
    framework: Framework = Framework.CAIRO


class Endpoint(BaseModel):
    id: int
    status: Optional[str] = None
    uri: Optional[str] = None
    size: ServiceSize
    service_name: Optional[str] = None
    model_id: Optional[int] = None
    version_id: Optional[int] = None

    class Config:
        orm_mode = True


class EndpointsList(BaseModel):
    __root__: list[Endpoint]
