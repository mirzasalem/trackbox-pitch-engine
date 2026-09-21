"""Structured logging setup for unattended, batch-run pipeline execution.

The pipeline runs with no one watching the console, so every log line needs
enough context (timestamp, level, module, run id) for someone to reconstruct
what happened after the fact, without attaching a debugger.
"""

import logging
import sys
import uuid


def configure_logging(debug_mode: bool = False) -> logging.LoggerAdapter:
    """Configure root logging and return a logger tagged with a unique run id.

    Every log line from the returned logger carries the same run_id, so all
    output from a single execution can be grepped/filtered together even
    when logs from multiple runs are interleaved (e.g. in a shared log file
    or a log aggregator).
    """
    level = logging.DEBUG if debug_mode else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s [run=%(run_id)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )

    run_id = uuid.uuid4().hex[:8]
    base_logger = logging.getLogger("pitch_engine")
    return logging.LoggerAdapter(base_logger, {"run_id": run_id})
