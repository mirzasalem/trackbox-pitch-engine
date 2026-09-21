"""Structured logging setup for unattended, batch-run pipeline execution.

The pipeline runs with no one watching the console, so every log line needs
enough context (timestamp, level, module, run id) for someone to reconstruct
what happened after the fact, without attaching a debugger.
"""

import logging
import sys
import uuid


class _DefaultRunIdFilter(logging.Filter):
    """Ensures every record has a run_id, even ones from third-party loggers
    (e.g. requests/urllib3) that never pass through our LoggerAdapter.
    Without this, the formatter below raises KeyError on any log line that
    doesn't carry a run_id.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "run_id"):
            record.run_id = "-"
        return True


def configure_logging(debug_mode: bool = False) -> logging.LoggerAdapter:
    """Configure root logging and return a logger tagged with a unique run id.

    Every log line from the returned logger carries the same run_id, so all
    output from a single execution can be grepped/filtered together even
    when logs from multiple runs are interleaved (e.g. in a shared log file
    or a log aggregator).
    """
    level = logging.DEBUG if debug_mode else logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-8s [run=%(run_id)s] %(name)s: %(message)s")
    )
    handler.addFilter(_DefaultRunIdFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]  # avoid duplicate handlers if called twice

    # Third-party HTTP libraries are extremely chatty at DEBUG level and add
    # little value to our own observability — keep them quiet regardless of
    # our own debug_mode.
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    run_id = uuid.uuid4().hex[:8]
    base_logger = logging.getLogger("pitch_engine")
    adapter = logging.LoggerAdapter(base_logger, {"run_id": run_id})
    return adapter, run_id

