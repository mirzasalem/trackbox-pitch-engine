from unittest.mock import patch, Mock

import requests

from src.pitch_engine.reporting import ReportingClient
from src.pitch_engine.models import ProgressReport


class RecordingLogger:
    def __init__(self):
        self.warnings = []

    def info(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        self.warnings.append(args)

    def error(self, *args, **kwargs):
        pass


def test_report_progress_sends_request_when_successful():
    logger = RecordingLogger()
    client = ReportingClient(logger, base_url="http://fake-host")

    with patch("src.pitch_engine.reporting.requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=200, raise_for_status=lambda: None)

        client.report_progress(ProgressReport(run_id="r1", video_path="v.mp4", frames_processed=5))

        assert mock_post.called
        called_url = mock_post.call_args.args[0]
        assert called_url == "http://fake-host/api/v1/jobs/progress"
        assert logger.warnings == []


def test_report_failure_is_caught_not_raised():
    logger = RecordingLogger()
    client = ReportingClient(logger, base_url="http://fake-host")

    with patch(
        "src.pitch_engine.reporting.requests.post",
        side_effect=requests.exceptions.ConnectionError("boom"),
    ):
        client.report_progress(ProgressReport(run_id="r1", video_path="v.mp4", frames_processed=5))

        assert len(logger.warnings) == 1
