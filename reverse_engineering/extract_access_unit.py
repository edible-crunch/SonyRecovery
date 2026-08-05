from parsers.mdat_reader import locate_mdat

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

# First validated Sony sample fingerprint
START = 1560580

SEARCH_LIMIT = 8 * 1024 * 1024

mdat = locate_mdat(RECOVERED_MP4)

with open(RECOVERED_MP4, "rb") as f:

    f.seek(START)

    blob = f.read(SEARCH_LIMIT)

print("=" * 70)
print("ACCESS UNIT EXTRACTOR")
print("=" * 70)
print(f"Start Offset : {START:,}")
print()

#
# Verify first AUD
#

if blob[:4] != b"\x00\x00\x00\x03":
    print("ERROR: Does not begin with AUD length.")
    raise SystemExit

if blob[4:6] != b"\x46\x01":
    print("ERROR: Does not begin with AUD.")
    raise SystemExit

print("[OK] AUD verified")

#
# Walk NALs
#

pos = 0
nal_count = 0

while True:

    if pos + 4 > len(blob):
        print("\nReached end of buffer.")
        break

    length = int.from_bytes(blob[pos:pos+4], "big")

    if length <= 0:
        print("\nInvalid NAL length.")
        break

    if pos + 4 + length > len(blob):
        print("\nNAL exceeds buffer.")
        break

    nal_type = (blob[pos+4] >> 1) & 0x3F

    print(
        f"{nal_count+1:03d}  "
        f"Offset {START+pos:,}  "
        f"Type {nal_type:2d}  "
        f"Length {length:,}"
    )

    pos += 4 + length
    nal_count += 1

    #
    # Search for next Sony sample fingerprint
    #

    if pos + 12 >= len(blob):
        break

    if (
        blob[pos:pos+4] == b"\x00\x00\x00\x03"
        and
        blob[pos+4:pos+6] == b"\x46\x01"
    ):

        #
        # Verify next SEI
        #

        p = pos + 7

        if p + 6 < len(blob):

            sei_length = int.from_bytes(
                blob[p:p+4],
                "big"
            )

            if (
                sei_length > 0
                and
                blob[p+4:p+6] == b"\x4E\x01"
            ):

                print()
                print("=" * 70)
                print("NEXT SONY SAMPLE FOUND")
                print("=" * 70)
                print(f"Next Sample Offset : {START+pos:,}")
                print(f"Current Sample Size: {pos:,} bytes")
                break

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"NALs Parsed : {nal_count}")
print(f"Bytes Walked: {pos:,}")