# Decisions

## Assumptions & Open Questions

- The mock detector identifies the green field area, not the white boundary
  lines. So a close-up/no-pitch frame and a valid pitch frame may produce the
  same polygon.
- Open question: How will the real ML model distinguish a genuine "no field
  visible" frame from a valid but low-confidence detection?
