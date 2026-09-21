
import json
from src.pitch_engine.models import RunSummary

from pydantic import BaseModel, Field


class FieldDetectorConfig(BaseModel):
    type: str
    sport: str
    min_area: int = Field(gt=0)


class PipelineConfig(BaseModel):
    video_path: str
    target_fps: int = Field(gt=0)
    confidence_threshold: float = Field(ge=0.0, le=1.0)
    field_detector: FieldDetectorConfig
    debug_mode: bool = False

    @classmethod
    def from_json(cls, json_path: str) -> "PipelineConfig":
        with open(json_path, "r") as f:
            data = json.load(f)
        return cls.model_validate(data)
