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