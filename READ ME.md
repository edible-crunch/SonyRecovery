# SonyRecovery

SonyRecovery is a reverse-engineering and reconstruction framework for damaged Sony HEVC MP4 recordings.

## Status
- Reverse engineering: Complete
- Reconstruction: Complete
- Validation: Complete
- Integration: In Progress

## Pipeline

Recovered MOV
→ rebuild_stsz.txt
→ rebuilt_stsz.bin
→ generate_offsets()
→ build STCO atoms
→ patch_moov_v2.py
→ patched_moov.bin
→ candidate_clip3.mp4
→ ffprobe
→ VLC
→ Premiere

See the docs folder for detailed project documentation.


Milestone: M1 - First End-to-End Recovery

☑ Reverse engineering
☑ Reconstruction
☑ Validation
☑ Documentation
☑ Repository organization
⬜ patch_moov_v2.py
⬜ patched_moov.bin
⬜ candidate_clip3.mp4
⬜ ffprobe validation
⬜ Premiere import