import os

import pytest
from shapely.geometry import Polygon

from synthetic_generator import generate_synthetic_video
from src.pitch_engine.config import PipelineConfig, FieldDetectorConfig
from src.pitch_engine.pipeline import FieldBoundaryAnalyzer

TEST_VIDEO = "test_pipeline_feed.mp4"


@pytest.fixture(scope="module", autouse=True)
def small_video():
    generate_synthetic_video(TEST_VIDEO, numFrames=30, seed=1)
    yield
    if os.path.exists(TEST_VIDEO):
        os.remove(TEST_VIDEO)


class NullLogger:
    def info(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass


class NullReportingClient:
    def report_progress(self, *args, **kwargs):
        pass

    def report_event(self, *args, **kwargs):
        pass


class AlwaysValidDetector:
    def detect(self, frame):
        return Polygon([(100, 100), (1180, 100), (1180, 600), (100, 600)])


class AlwaysNoneDetector:
    def detect(self, frame):
        return None


def make_config():
    return PipelineConfig(
        video_path=TEST_VIDEO,
        target_fps=30,
        confidence_threshold=0.5,
        field_detector=FieldDetectorConfig(type="test", sport="football", min_area=1000),
        debug_mode=False,
    )
def test_valid_detections_are_counted():
    config = make_config()
    analyzer = FieldBoundaryAnalyzer(
        config, AlwaysValidDetector(), NullLogger(), NullReportingClient(), "test-run"
    )
    summary = analyzer.process_video(TEST_VIDEO)

    assert summary is not None
    assert summary.valid_count == summary.sampled_frames
    assert summary.invalid_count == 0
    assert summary.no_detection_count == 0
    assert summary.average_valid_area is not None


def test_no_detection_frames_are_counted():
    config = make_config()
    analyzer = FieldBoundaryAnalyzer(
        config, AlwaysNoneDetector(), NullLogger(), NullReportingClient(), "test-run"
    )
    summary = analyzer.process_video(TEST_VIDEO)

    assert summary.no_detection_count == summary.sampled_frames
    assert summary.valid_count == 0
    assert summary.average_valid_area is None


def test_missing_video_returns_none():
    config = make_config()
    analyzer = FieldBoundaryAnalyzer(
        config, AlwaysValidDetector(), NullLogger(), NullReportingClient(), "test-run"
    )
    result = analyzer.process_video("does_not_exist.mp4")

    assert result is None
