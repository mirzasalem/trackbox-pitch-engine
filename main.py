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
    # The video itself couldn't be opened: this is a fatal failure, not a
    # zero-detection run. Exit non-zero so an orchestrator can tell the
    # difference instead of reading a clean exit as success.
    logger.error("Pipeline failed: video could not be opened.")
    sys.exit(1)

logger.info(f"Pipeline finished with {len(results)} results.")