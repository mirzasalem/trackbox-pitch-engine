from src.pitch_engine.config import PipelineConfig

from src.pitch_engine.detectors.mask_detector import HsvMaskFieldDetector
from src.pitch_engine.pipeline import FieldBoundaryAnalyzer
config = PipelineConfig.from_json("config.json")
print(config)

detector = HsvMaskFieldDetector(min_area=config.field_detector.min_area)
analyzer = FieldBoundaryAnalyzer(config, detector)

results = analyzer.process_video(config.video_path)
print(f"Pipeline finished with {len(results) if results else 0} results.")