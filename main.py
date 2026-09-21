import sys

from src.pitch_engine.config import PipelineConfig
from src.pitch_engine.detectors.mask_detector import HsvMaskFieldDetector
from src.pitch_engine.pipeline import FieldBoundaryAnalyzer
from src.pitch_engine.logging_setup import configure_logging
from src.pitch_engine.reporting import ReportingClient
from src.pitch_engine.models import JobEvent

config = PipelineConfig.from_json("config.json")
logger, run_id = configure_logging(debug_mode=config.debug_mode)
logger.info(f"loaded config: {config}")

detector = HsvMaskFieldDetector(min_area=config.field_detector.min_area)
reporting_client = ReportingClient(logger)
analyzer = FieldBoundaryAnalyzer(config, detector, logger, reporting_client, run_id)

results = analyzer.process_video(config.video_path)

if results is None:
    reporting_client.report_event(
        JobEvent(run_id=run_id, video_path=config.video_path, status="failed", error_message="video could not be opened")
    )
    logger.error("Pipeline failed: video could not be opened.")
    sys.exit(1)

reporting_client.report_event(
    JobEvent(run_id=run_id, video_path=config.video_path, status="success", summary=results)
)
logger.info(
    f"Pipeline finished: {results.valid_count} valid, "
    f"{results.invalid_count} invalid, {results.no_detection_count} no-detection, "
    f"{results.failed_count} failed (of {results.sampled_frames} sampled frames)."
)
