from parsers.mdat_reader import locate_mdat
from repair.hvcc import parse_hvcc


def find_first(data, pattern):

    return data.find(pattern)


mp4 = input("Recovered MP4:\n").strip('"')

hvcc = input("HVCC BIN:\n").strip('"')

mdat = locate_mdat(mp4)

cfg = parse_hvcc(hvcc)

# -------------------------------
# Find VPS automatically
# -------------------------------

vps = None

for array in cfg.arrays:

    if array["type"] == 32:

        vps = array["nalus"][0]
        break

if vps is None:

    raise Exception("No VPS found.")

with open(mp4, "rb") as f:

    f.seek(mdat.data_offset)

    payload = f.read(mdat.size)

relative = find_first(payload, vps)

if relative == -1:

    raise Exception("VPS not found.")

anchor = mdat.data_offset + relative

window = 512

start = anchor - window

end = anchor + window

with open(mp4, "rb") as f:

    f.seek(start)

    data = f.read(end - start)

print()
print("=" * 80)
print("CHUNK ANCHOR")
print("=" * 80)

print()
print(f"MDAT Payload : {mdat.data_offset:,}")
print(f"VPS Relative : {relative:,}")
print(f"Anchor       : {anchor:,}")
print()

for i in range(0, len(data), 16):

    absolute = start + i

    chunk = data[i:i+16]

    hexs = " ".join(
        f"{b:02X}" for b in chunk
    )

    text = "".join(
        chr(b) if 32 <= b < 127 else "."
        for b in chunk
    )

    marker = ""

    if absolute == anchor:

        marker = " <<< VPS"

    print(
        f"{absolute:08X}  "
        f"{hexs:<47} "
        f"{text}"
        f"{marker}"
    )