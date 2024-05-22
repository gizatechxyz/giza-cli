from pydantic import BaseModel


class Logs(BaseModel):
    logs: str
