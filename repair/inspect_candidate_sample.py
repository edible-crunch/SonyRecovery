from parsers.video_tables import get_video_tables
from parsers.mdat_reader import locate_mdat

MP4 = "candidate_clip3.mp4"

tables = get_video_tables(MP4)

mdat = locate_mdat(MP4)

print("=" * 70)
print("CANDIDATE MP4")
print("=" * 70)

print()
print("mdat payload :", mdat.data_offset)

offset = tables["stco"].offsets[0]
size = tables["stsz"][0]

print()
print("First sample")
print("Offset :", offset)
print("Size   :", size)

with open(MP4, "rb") as f:

    f.seek(offset)

    data = f.read(128)

print()
print("Read bytes :", len(data))

print()
print("First 64 bytes")
print("-" * 70)

for i in range(0, len(data[:64]), 16):

    row = data[i:i+16]

    print(
        f"{i:04X}  "
        + " ".join(f"{b:02X}" for b in row)
    )

print()

if len(data) >= 4:

    length = int.from_bytes(data[:4], "big")

    print("First length :", length)

if len(data) >= 6:

    h0 = data[4]
    h1 = data[5]

    print("Header bytes :", f"{h0:02X} {h1:02X}")

    nal_type = (h0 >> 1) & 0x3F

    print("NAL type :", nal_type)

print()

print("Searching for Annex-B start codes...")

count = 0

for i in range(len(data)-4):

    if data[i:i+4] == b"\x00\x00\x00\x01":

        print("00000001 at", i)
        count += 1

    elif data[i:i+3] == b"\x00\x00\x01":

        print("000001 at", i)
        count += 1

print()

print("Start codes found :", count)