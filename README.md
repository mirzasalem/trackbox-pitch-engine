# Pitch Boundary Pipeline

Batch pipeline that reads a match video, detects the pitch boundary on
sampled frames, classifies each detection as valid / invalid / missing,
and reports progress and the final result to a reporting service over HTTP.

Refactored from the original prototype (`synthetic_field_prototype.py`,
kept unchanged for reference). Design decisions and known limitations are
in [DECISIONS.md](DECISIONS.md).

## Project layout

```
main.py                     entry point: load config, wire dependencies, run, exit code
config.json                 pipeline settings (validated at startup)
src/pitch_engine/
  config.py                 Pydantic config model, fails fast on bad input
  detectors/base.py         FieldDetector interface (the swappable seam)
  detectors/mask_detector.py  HSV mask detector (mock implementation)
  pipeline.py               frame sampling, detection, classification, aggregation
  models.py                 RunSummary, ProgressReport, JobEvent
  reporting.py              HTTP client for the reporting service
  logging_setup.py          structured logs tagged with a per-run id
tests/                      config, pipeline and reporting tests
mock_api/                   reporting service (unchanged)
```

## Run with Docker (recommended)

```bash
docker compose up --build
```

This starts `mock_api` and the `runner`. The runner generates the synthetic
video if it isn't present, processes it, reports to `mock_api` over the
compose network and exits. Check what was reported:

```bash
curl http://localhost:5050/api/v1/jobs/events
```

`mock_api` is mapped to host port 5050 because macOS AirPlay Receiver
uses port 5000.

## Run locally

Requires Python 3.12+.

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

The reporting service URL comes from `MOCK_API_URL`
(default `http://localhost:5000`). If the service isn't reachable, the
pipeline logs a warning and still completes.

## Tests

```bash
pytest tests/ -v
```

## Configuration

Settings live in `config.json`: `video_path`, `target_fps`,
`confidence_threshold` and `field_detector` (`type`, `sport`, `min_area`).
A missing or invalid value stops the run at startup with a validation
error. Only `debug_mode` has a default.

## Exit codes

- `0`: the video was processed (including runs with zero valid detections)
- non-zero: invalid config, or the video could not be opened

## Reporting

- `POST /api/v1/jobs/progress` every 200 frames
- `POST /api/v1/jobs/events` once at the end, with `status` (`success` or
  `failed`) and the run summary
