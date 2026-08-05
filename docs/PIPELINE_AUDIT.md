# SonyRecovery Pipeline Audit

**Status:** Complete
**Date:** 2026-08-05
**Purpose:** Audit the production pipeline before implementing `patch_moov_v2.py`.

---

# Goal

Verify every production module before integration.

The objective of this audit was to determine:

- Which modules are production-ready.
- Which modules require refactoring.
- Which legacy code should be retired.
- Which components will form the final repair pipeline.

---

# Audit Results

| Module | Status | Decision |
|---------|--------|----------|
| parsers/atom_reader.py | ✅ Production Ready | Freeze |
| parsers/track_locator.py | 🟡 Minor Enhancement | Decode handler types (`vide`, `soun`, `meta`) |
| repair/moov_editor.py | ✅ Production Ready | Freeze |
| repair/stco_generator.py | ✅ Production Ready | Freeze |
| repair/build_stco_atom.py | 🟡 Refactor | Convert into reusable `build_stco_atom(offsets)` function |
| patch_moov.py | 🔄 Legacy | Replace with `patch_moov_v2.py` |

---

# Frozen Modules

The following modules are considered stable and should not be modified unless an
integration test proves they are incorrect.

## parsers/atom_reader.py

Responsibilities

- Read MP4 atoms recursively
- Produce `Atom` objects
- Maintain absolute offsets

Status

- Production Ready

---

## repair/moov_editor.py

Responsibilities

- Replace atoms
- Patch parent atom sizes
- Save modified MOOV

Status

- Production Ready

---

## repair/stco_generator.py

Responsibilities

- Read rebuilt STSZ
- Calculate synchronized Meta / Video / Audio chunk offsets

Status

- Production Ready

---

# Modules Requiring Minor Work

## parsers/track_locator.py

Current

Returns track structures.

Future

Should identify tracks by handler type:

- `vide`
- `soun`
- `meta`

instead of relying on track order.

---

## repair/build_stco_atom.py

Current

Prototype utility that writes STCO atoms to disk.

Future

Should expose a reusable function:

```python
build_stco_atom(offsets) -> bytes
```

The function should return the complete STCO atom without writing files.

---

# Legacy Components

These are no longer part of the production architecture.

- chunk_starts.txt
- rebase_offsets()
- MDAT_DELTA
- write_stco()
- Manual STCO rebasing

These were replaced by:

```
generate_offsets()
↓

build_stco_atom()

↓

replace_atom()
```

---

# Final Production Pipeline

```
Recovered MOV
        │
        ▼
Rebuild STSZ
        │
        ▼
Generate synchronized offsets
        │
        ▼
Build STCO atoms
        │
        ▼
Open MOOV
        │
        ├── Replace Video STSZ
        ├── Replace Video STCO
        ├── Replace Audio STCO
        └── Replace Metadata STCO
                │
                ▼
Patch parent sizes
                │
                ▼
patched_moov.bin
                │
                ▼
candidate_clip3.mp4
                │
                ▼
Validation
```

---

# Engineering Decisions

The following decisions are locked unless new evidence proves them incorrect.

- STSZ reconstruction is authoritative.
- `generate_offsets()` is the production source of truth.
- `MoovEditor` is the production patch engine.
- `track_locator.py` is the authoritative track discovery module.
- Parent atom sizes are updated only through `MoovEditor`.
- No new reverse-engineering utilities should be created unless an integration failure requires additional investigation.

---

# Next Milestone

Implement:

```
patch_moov_v2.py
```

Responsibilities:

- Discover tracks
- Load rebuilt STSZ
- Generate synchronized offsets
- Build replacement STCO atoms
- Replace STSZ and STCO atoms
- Patch parent sizes
- Save `patched_moov.bin`

After implementation:

1. Build `candidate_clip3.mp4`
2. Validate with `ffprobe`
3. Test in VLC
4. Test in Premiere
