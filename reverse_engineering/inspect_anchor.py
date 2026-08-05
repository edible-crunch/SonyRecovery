from parsers.mdat_reader import locate_mdat
from repair.hevc import parse_header

WINDOW_BEFORE = 512
WINDOW_AFTER = 4096

mp4 = input("Recovered MP4:\n").strip('"')

anchor = int(input("Anchor Offset (inside mdat): "))

mdat = locate_mdat(mp4)

absolute = mdat.data_offset + anchor

print()
print("=" * 60)
print("ANCHOR INSPECTION")
print("=" * 60)

print(f"MDAT Payload : {mdat.data_offset:,}")
print(f"Anchor       : {anchor:,}")
print(f"Absolute     : {absolute:,}")

with open(mp4, "rb") as f:

    f.seek(absolute - WINDOW_BEFORE)

    data = f.read(WINDOW_BEFORE + WINDOW_AFTER)

print()
print("Searching for NAL length/header pairs...")
print()

for i in range(len(data) - 6):

    nal_length = int.from_bytes(
        data[i:i+4],
        "big"
    )

    if nal_length <= 0:
        continue

    if nal_length > 10_000_000:
        continue

    header = parse_header(data[i+4:i+6])

    if header is None:
        continue

    if header["forbidden_zero"] != 0:
        continue

    if header["layer_id"] != 0:
        continue

    if header["temporal_id"] <= 0:
        continue

    print(
        f"{i-WINDOW_BEFORE:+6d} "
        f"len={nal_length:8d} "
        f"{header['nal_name']}"
    )