import json
import pytest
from src.pitch_engine.config import PipelineConfig


VALID_DATA = {
    "video_path": "synthetic_pitch_feed.mp4",
    "target_fps": 30,
    "confidence_threshold": 0.5,
    "field_detector": {"type": "sam_mask_v1", "sport": "football", "min_area": 1000},
    "debug_mode": True,
}


def test_valid_config_loads():
    config = PipelineConfig.model_validate(VALID_DATA)
    assert config.target_fps == 30
    assert config.field_detector.sport == "football"


def test_invalid_target_fps_raises():
    bad_data = {**VALID_DATA, "target_fps": -5}
    with pytest.raises(Exception):
        PipelineConfig.model_validate(bad_data)


def test_missing_required_field_raises():
    bad_data = {**VALID_DATA}
    del bad_data["video_path"]
    with pytest.raises(Exception):
        PipelineConfig.model_validate(bad_data)
