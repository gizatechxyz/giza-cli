from typing import Optional

from pydantic import BaseModel, ConfigDict, RootModel

from giza.cli.utils.enums import Framework, ServiceSize


class EndpointCreate(BaseModel):
    file: Optional[str] = None
    uri: Optional[str] = None
    model_id: Optional[int] = None
    version_id: Optional[int] = None
    status: Optional[str] = None
    size: ServiceSize
    service_name: Optional[str] = None
    framework: Framework = Framework.CAIRO

    model_config = ConfigDict(from_attributes=True)
    model_config["protected_namespaces"] = ()


class Endpoint(BaseModel):
    id: int
    status: Optional[str] = None
    uri: Optional[str] = None
    size: ServiceSize
    service_name: Optional[str] = None
    model_id: Optional[int] = None
    version_id: Optional[int] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
    model_config["protected_namespaces"] = ()


class EndpointsList(RootModel):
    root: list[Endpoint]
