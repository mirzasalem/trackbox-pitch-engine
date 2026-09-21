from typing import Protocol
import numpy as np
from shapely.geometry import Polygon


class FieldDetector(Protocol):
    def detect(self, frame: np.ndarray) -> Polygon | None:
        """Return the detected field-boundary polygon for a frame or None if not found."""
        ...
