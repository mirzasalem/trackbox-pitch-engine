from pydantic import BaseModel

class RunSummary(BaseModel):
    total_frames: int
    sampled_frames: int
    valid_count: int
    invalid_count: int
    no_detection_count: int
    failed_count: int
    average_valid_area: float | None
