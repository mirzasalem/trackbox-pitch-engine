# Decisions

## Assumptions & Open Questions

- The mock detector identifies the green field area, not the white boundary
  lines. So a close-up/no-pitch frame and a valid pitch frame may produce the
  same polygon.
- Open question: How will the real ML model distinguish a genuine "no field
  visible" frame from a valid but low-confidence detection?


## Performance Trade-offs

- Used `cap.grab()` with conditional `retrieve()` so only selected frames
  are decoded and analyzed, improving speed.
- Built the video boundary once using the actual resolution instead of
  recreating it for every frame.
- On a 3600-frame test, processing took ~3.0s at 30 FPS and ~1.1s at 10 FPS.
- The trade-off is that frame sampling can miss very brief boundary issues,
  but this is acceptable for long continuous feeds where overall throughput
  is more important.
