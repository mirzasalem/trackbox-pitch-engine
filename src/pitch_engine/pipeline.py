import cv2
from shapely.geometry import Polygon

from src.pitch_engine.config import PipelineConfig
from src.pitch_engine.detectors.base import FieldDetector
from src.pitch_engine.models import RunSummary


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
        frame_area = frame_width * frame_height
        outer_boundary = Polygon(
            [(0, 0), (frame_width, 0), (frame_width, frame_height), (0, frame_height)]
        )

        source_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        sample_interval = max(1, round(source_fps / self.config.target_fps))

        frame_count = 0
        failed_frame_count = 0
        valid_count = 0
        invalid_count = 0
        no_detection_count = 0
        valid_areas = []

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

            if poly is None:
                no_detection_count += 1
                continue

            intersection_area = poly.intersection(outer_boundary).area
            area_ratio = intersection_area / frame_area

            if not poly.is_valid or area_ratio > 0.95:
                invalid_count += 1
            else:
                valid_count += 1
                valid_areas.append(intersection_area)

        cap.release()

        average_valid_area = sum(valid_areas) / len(valid_areas) if valid_areas else None

        summary = RunSummary(
            total_frames=frame_count,
            sampled_frames=valid_count + invalid_count + no_detection_count,
            valid_count=valid_count,
            invalid_count=invalid_count,
            no_detection_count=no_detection_count,
            failed_count=failed_frame_count,
            average_valid_area=average_valid_area,
        )

        self.logger.info(f"Run summary: {summary}")
        return summary
