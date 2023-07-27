from enum import StrEnum


class ModelStatus(StrEnum):
    COMPLETED: str = "COMPLETED"
    FAILED: str = "FAILED"
    STARTING: str = "STARTING"
    UPLOADED: str = "UPLOADED"
    PROCESSING: str = "PROCESSING"
