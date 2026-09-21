import cv2
from shapely.geometry import Polygon

from src.pitch_engine.config import PipelineConfig
from src.pitch_engine.detectors.base import FieldDetector


class FieldBoundaryAnalyzer:
    def __init__(self, config: PipelineConfig, detector: FieldDetector, logger):
        self.config = config
        self.detector = detector
        self.logger = logger

    def process_video(self, video_path: str):
        self.logger.info(f"Starting processing for video: {video_path}")
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            self.logger.error(f"Could not open video stream: {video_path}")
            return None

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        outer_boundary = Polygon(
            [(0, 0), (frame_width, 0), (frame_width, frame_height), (0, frame_height)]
        )

        source_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        sample_interval = max(1, round(source_fps / self.config.target_fps))

        frame_count = 0
        detected_polygons = []
        failed_frame_count = 0

        while True:
            ret = cap.grab()
            if not ret:
                break

            frame_count += 1

            if frame_count % sample_interval != 0:
                continue

            ret, frame = cap.retrieve()
            if not ret:
                break

            try:
                poly = self.detector.detect(frame)
            except Exception:
                # A single bad/corrupt frame is a recoverable failure: log it
                # and keep processing the rest of the feed, don't crash the
                # whole run over one frame.
                failed_frame_count += 1
                self.logger.warning(
                    f"Detector raised on frame {frame_count}, skipping frame",
                    exc_info=True,
                )
                continue

            if poly and poly.is_valid:
                intersection_area = poly.intersection(outer_boundary).area
                detected_polygons.append((frame_count, poly, intersection_area))

        cap.release()
        self.logger.info(
            f"Processed {frame_count} frames. Found {len(detected_polygons)} boundaries. "
            f"{failed_frame_count} frames failed detection."
        )
        return detected_polygons
