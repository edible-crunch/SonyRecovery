from parsers.video_tables import get_video_tables
from recovery.frame_mapper import build_frame_map

HEALTHY_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\C0946.MP4"

tables = get_video_tables(HEALTHY_MP4)

frame_map = build_frame_map(
    tables["stco"].offsets,
    tables["stsc"],
    tables["stsz"]
)

frame = frame_map[0]

print("=" * 70)
print("HEALTHY FRAME 1")
print("=" * 70)

print("Offset :", frame["offset"])
print("Size   :", frame["size"])

with open(HEALTHY_MP4, "rb") as f:
    f.seek(frame["offset"])
    sample = f.read(frame["size"])

print("Bytes read :", len(sample))
print()

pos = 0

for nal in range(1, 6):

    if pos + 4 > len(sample):
        break

    print("=" * 60)
    print(f"NAL {nal}")
    print("=" * 60)

    blob = sample[pos:pos+32]

    for i in range(0, len(blob), 16):
        row = blob[i:i+16]
        print(
            f"{pos+i:08X}  "
            + " ".join(f"{b:02X}" for b in row)
        )

    length = int.from_bytes(sample[pos:pos+4], "big")

    print()
    print("Length :", length)

    if length == 0:
        print("ZERO LENGTH")
        break

    if pos + 4 + length > len(sample):
        print("EXCEEDS SAMPLE")
        break

    header = sample[pos + 4]

    print("NAL Type :", (header >> 1) & 0x3F)

    pos += 4 + length

print()
print("Finished.")