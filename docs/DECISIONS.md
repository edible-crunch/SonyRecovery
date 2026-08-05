# Locked Decisions

- Sony mux order is fixed.
- generate_offsets() is the production source of truth.
- track_locator.py is the authoritative parser.
- stco_writer.py is legacy.
- No hard-coded STCO offsets.
- Avoid creating new utilities unless integration testing requires them.
