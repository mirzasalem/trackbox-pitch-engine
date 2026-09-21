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
logger.info(f"Pipeline finished with {len(results) if results else 0} results.")