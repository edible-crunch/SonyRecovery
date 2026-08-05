from parsers.mdat_reader import locate_mdat

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

# Absolute file offset we validated
START = 1429508

mdat = locate_mdat(RECOVERED_MP4)

with open(RECOVERED_MP4, "rb") as f:

    f.seek(START)

    blob = f.read(4 * 1024 * 1024)

print("=" * 70)
print("CANDIDATE WALK")
print("=" * 70)
print(f"Starting offset : {START:,}")
print()

pos = 0

for i in range(300):

    if pos + 4 > len(blob):
        print("\nReached end of buffer.")
        break

    length = int.from_bytes(blob[pos:pos+4], "big")

    if length <= 0:
        print(f"\nStopped: invalid length {length}")
        break

    if pos + 4 + length > len(blob):
        print(f"\nStopped: length {length:,} exceeds remaining buffer.")
        break

    header = blob[pos + 4]

    nal_type = (header >> 1) & 0x3F

    print(
        f"{i+1:03d}  "
        f"Offset {START + pos:,}  "
        f"Length {length:,}  "
        f"Type {nal_type}"
    )

    pos += 4 + length

print()
print("=" * 70)
print("Finished")
print("=" * 70)
print(f"NALs parsed : {i+1}")
print(f"Bytes walked: {pos:,}")