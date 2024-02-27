from typing import Optional

from pydantic import BaseModel, ConfigDict, RootModel

from giza.utils.enums import Framework, ServiceSize


class DeploymentCreate(BaseModel):
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


class Deployment(BaseModel):
    id: int
    status: Optional[str] = None
    uri: Optional[str] = None
    size: ServiceSize
    service_name: Optional[str] = None
    model_id: Optional[int] = None
    version_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
    model_config["protected_namespaces"] = ()


class DeploymentsList(RootModel):
    root: list[Deployment]
