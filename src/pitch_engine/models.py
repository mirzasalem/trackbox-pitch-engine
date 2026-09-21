from pydantic import BaseModel, Field
from datetime import datetime, timezone

class RunSummary(BaseModel):
    total_frames: int
    sampled_frames: int
    valid_count: int
    invalid_count: int
    no_detection_count: int
    failed_count: int
    average_valid_area: float | None

class ProgressReport(BaseModel):
    run_id: str
    video_path: str
    frames_processed: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobEvent(BaseModel):
    run_id: str
    video_path: str
    status: str  # "success" or "failed"
    summary: RunSummary | None = None
    error_message: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
