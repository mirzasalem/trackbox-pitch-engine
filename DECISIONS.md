# Decisions

## Assumptions & Open Questions

- The mock detector only detects the green area, so it returns a near full-frame polygon instead of the actual pitch boundary.
- In the 1800-frame test: 0 valid, 1776 invalid, and 24 no-detection frames.
- This confirms area alone cannot distinguish a visible pitch from a close-up/no-pitch frame.
- Open question: How will the real ML model identify “no field visible” vs. a valid          low-confidence detection?


## Performance Trade-offs

- Used `cap.grab()` with conditional `retrieve()` so only selected frames
  are decoded and analyzed, improving speed.
- Built the video boundary once using the actual resolution instead of
  recreating it for every frame.
- On a 3600-frame test, processing took ~3.0s at 30 FPS and ~1.1s at 10 FPS.
- The trade-off is that frame sampling can miss very brief boundary issues,
  but this is acceptable for long continuous feeds where overall throughput
  is more important.


## Validation Strictness vs. Fallback
- Config: Invalid or missing pipeline settings fail immediately. Only debug_mode has a default.
- Frame data: Bad or missing detections are counted and skipped, so one bad frame doesn't stop the whole video.
- Threshold: The 0.95 area-ratio rule is currently a fixed heuristic and rejects all frames with the mock detector.
- This is kept as a known limitation rather than tuning the threshold just to produce better-looking results.
- Reporting failures are treated separately from pipeline failures: a network error while calling mock_api (connection refused, timeout, bad status) is caught inside ReportingClient, logged as a warning, and does not affect the pipeline's own exit code or result. Verified this by running the pipeline with mock_api stopped — it completed and exited 0 normally, only logging that the report couldn't be sent.
- MOCK_API_URL is read from an environment variable, not from the strict PipelineConfig model — it's deployment wiring (differs between local runs and the docker-compose network), not pipeline domain config.


## AI/LLM Disclosure


- I used AI tools, primarily Claude Code and ChatGPT, as development assistants, guides, and reviewers throughout this work.

- I wrote and reviewed most of the implementation myself, including the configuration model, detector interface and mask detector, pipeline refactor, frame sampling, validity and aggregation logic, Pydantic report models, reporting client, and the test suite. Before implementing each major change, I used Claude Code or ChatGPT to understand the proposed approach, discuss the reasoning and trade-offs, and then implemented and tested the changes myself.

- Claude Code directly generated a few supporting components, including the logging setup, subsequent logging fix for a formatter crash caused by third-party log lines, fatal/recoverable error-handling changes, the Dockerfile, and the Docker Compose runner service. It also reviewed my implementation and identified issues such as missing imports, a method-name mismatch, and an indentation error, which I then corrected.

- ChatGPT was also used for technical guidance, reviewing implementation decisions, clarifying concepts, and discussing possible approaches during development.

- The key engineering decisions remained mine. These included remapping mock_api to host port 5050 to avoid the macOS AirPlay port conflict, reporting the detector's 0-valid result honestly rather than adjusting the threshold to obtain a desired outcome, structuring the work into incremental commits, and deciding which implementation trade-offs to accept.

- Overall, AI tools were used as development aids and reviewers, while I remained responsible for the implementation, testing, debugging, and final engineering decisions.