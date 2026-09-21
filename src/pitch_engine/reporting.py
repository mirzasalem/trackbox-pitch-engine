import os

import requests
from pydantic import BaseModel

from src.pitch_engine.models import ProgressReport, JobEvent


class ReportingClient:
    def __init__(self, logger, base_url: str | None = None, timeout: float = 5.0):
        self.logger = logger
        self.base_url = base_url or os.environ.get("MOCK_API_URL", "http://localhost:5000")
        self.timeout = timeout

    def report_progress(self, report: ProgressReport) -> None:
        self._post("/api/v1/jobs/progress", report)

    def report_event(self, event: JobEvent) -> None:
        self._post("/api/v1/jobs/events", event)

    def _post(self, path: str, payload: BaseModel) -> None:
        url = f"{self.base_url}{path}"
        try:
            response = requests.post(url, json=payload.model_dump(mode="json"), timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            # A failure to reach the reporting service is NOT a pipeline
            # failure — log it and let the pipeline keep running.
            self.logger.warning(f"Failed to report to {url}", exc_info=True)
