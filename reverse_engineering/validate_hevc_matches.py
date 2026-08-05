from parsers.mdat_reader import locate_mdat

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

SCAN_SIZE = 16 * 1024 * 1024

PATTERNS = {
    b"\x40\x01": "VPS",
    b"\x42\x01": "SPS",
    b"\x44\x01": "PPS",
    b"\x46\x01": "AUD",
    b"\x4E\x01": "SEI",
    b"\x26\x01": "IDR",
    b"\x28\x01": "IDR_N_LP",
    b"\x2A\x01": "CRA",
}

mdat = locate_mdat(RECOVERED_MP4)

with open(RECOVERED_MP4, "rb") as f:

    f.seek(mdat.data_offset)

    blob = f.read(SCAN_SIZE)

print("=" * 70)
print("VALIDATING HEVC SIGNATURES")
print("=" * 70)
print(f"MDAT Payload Start : {mdat.data_offset:,}")
print()

found = 0

for i in range(4, len(blob) - 8):

    sig = blob[i:i+2]

    if sig not in PATTERNS:
        continue

    length = int.from_bytes(blob[i-4:i], "big")

    remaining = len(blob) - i

    # sanity checks
    if length <= 0:
        continue

    if length > remaining:
        continue

    if length > 10 * 1024 * 1024:
        continue

    print()

    print(f"Blob Offset : {i:,}")
    print(f"File Offset : {mdat.data_offset + i:,}")
    print(f"Type        : {PATTERNS[sig]}")
    print(f"Length      : {length:,}")

    print("Bytes around header:")

    start = max(i - 8, 0)
    end = min(i + 24, len(blob))

    data = blob[start:end]

    for j in range(0, len(data), 16):

        row = data[j:j+16]

        absolute = mdat.data_offset + start + j

        print(
            f"{absolute:08X}  "
            + " ".join(f"{b:02X}" for b in row)
        )

    found += 1

    if found >= 25:
        break

print()
print("Validated candidates:", found)