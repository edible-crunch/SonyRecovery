from recovery.chunk_parser import parse_chunk
from recovery.access_unit_parser import split_access_units

RECOVERED_MP4 = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000003.MP4"
)

# Reuse the exact CHUNK_STARTS list from test_stsz_builder.py
from test_stsz_builder import CHUNK_STARTS

print("=" * 100)
print("CHUNK MARKER AUDIT")
print("=" * 100)

total_frames = 0

for i in range(len(CHUNK_STARTS) - 1):

    start = CHUNK_STARTS[i]
    end = CHUNK_STARTS[i + 1]

    chunk = parse_chunk(
        RECOVERED_MP4,
        start,
        end
    )

    frames = split_access_units(chunk)

    total_frames += len(frames)

    status = "OK"

    if len(frames) != 60:
        status = "CHECK"

    print(
        f"{i+1:03d} | "
        f"Frames={len(frames):3d} | "
        f"Bytes={end-start:10,d} | "
        f"{status}"
    )

print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)

print(f"Markers           : {len(CHUNK_STARTS)}")
print(f"Intervals         : {len(CHUNK_STARTS)-1}")
print(f"Total frames      : {total_frames}")
print(f"Expected chunks   : {len(CHUNK_STARTS)-1}")