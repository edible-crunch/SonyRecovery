from parsers.mdat_reader import locate_mdat

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

# Scan first 16 MB of payload
SCAN_SIZE = 16 * 1024 * 1024

# Common HEVC NAL headers (second byte is usually 0x01 in Sony files)
patterns = {
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

print("=" * 70)
print("HEVC SIGNATURE SCAN")
print("=" * 70)
print(f"Payload starts at : {mdat.data_offset:,}")
print(f"Scanning          : {SCAN_SIZE:,} bytes")
print()

with open(RECOVERED_MP4, "rb") as f:

    f.seek(mdat.data_offset)

    blob = f.read(SCAN_SIZE)

matches = []

for i in range(len(blob) - 2):

    sig = blob[i:i+2]

    if sig in patterns:

        matches.append(
            (
                i,
                patterns[sig]
            )
        )

print(f"Matches found: {len(matches)}")
print()

for offset, name in matches[:200]:

    print(
        f"{offset:10,}   {name}"
    )

if len(matches) > 200:
    print()
    print(f"... {len(matches)-200} more")