from parsers.video_tables import get_video_tables
from recovery.frame_mapper import build_frame_map

RECOVERED_MOV = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mov\MOV_01m54s_000003.MOV"

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

SEARCH_RANGE = 65536        # ±64 KB

tables = get_video_tables(RECOVERED_MOV)

frame_map = build_frame_map(
    tables["stco"].offsets,
    tables["stsc"],
    tables["stsz"]
)

expected = frame_map[0]["offset"]

print()
print("=" * 70)
print("FRAME 1 ALIGNMENT SEARCH")
print("=" * 70)

print(f"Expected Offset : {expected:,}")
print(f"Search Range    : ±{SEARCH_RANGE:,} bytes")
print()

with open(RECOVERED_MP4, "rb") as f:

    start = max(0, expected - SEARCH_RANGE)

    f.seek(start)

    blob = f.read(SEARCH_RANGE * 2)

pattern = bytes([
    0x00,0x00,0x00,0x03,
    0x46,0x01
])

matches = 0

for i in range(len(blob)-len(pattern)):

    if blob[i:i+len(pattern)] == pattern:

        absolute = start + i

        print(
            f"Candidate @ {absolute:,} "
            f"(delta {absolute-expected:+,})"
        )

        matches += 1

print()

print("Matches:", matches)