import sys

from src.pitch_engine.config import PipelineConfig
from src.pitch_engine.detectors.mask_detector import HsvMaskFieldDetector
from src.pitch_engine.pipeline import FieldBoundaryAnalyzer
from src.pitch_engine.logging_setup import configure_logging

config = PipelineConfig.from_json("config.json")
logger = configure_logging(debug_mode=config.debug_mode)
logger.info(f"loaded config: {config}")


detector = HsvMaskFieldDetector(min_area=config.field_detector.min_area)
analyzer = FieldBoundaryAnalyzer(config, detector, logger)

results = analyzer.process_video(config.video_path)

if results is None:
    logger.error("Pipeline failed: video could not be opened.")
    sys.exit(1)

logger.info(
    f"Pipeline finished: {results.valid_count} valid, "
    f"{results.invalid_count} invalid, {results.no_detection_count} no-detection, "
    f"{results.failed_count} failed (of {results.sampled_frames} sampled frames)."
)
