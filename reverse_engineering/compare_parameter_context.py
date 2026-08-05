from parsers.mdat_reader import locate_mdat
from repair.hvcc import parse_hvcc


def load_payload(mp4):

    mdat = locate_mdat(mp4)

    with open(mp4, "rb") as f:

        f.seek(mdat.data_offset)

        payload = f.read(mdat.size - (mdat.data_offset - mdat.offset))

    return mdat, payload


healthy = input("Healthy MP4:\n").strip('"')
recovered = input("Recovered MP4:\n").strip('"')
hvcc_file = input("HVCC BIN:\n").strip('"')

cfg = parse_hvcc(hvcc_file)

vps = None

for arr in cfg.arrays:

    if arr["type"] == 32:

        vps = arr["nalus"][0]
        break

if vps is None:
    raise Exception("No VPS in hvcc.")

for title, mp4 in [
    ("HEALTHY", healthy),
    ("RECOVERED", recovered)
]:

    mdat, payload = load_payload(mp4)

    pos = payload.find(vps)

    if pos == -1:

        print(title, "VPS NOT FOUND")
        continue

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

    print("Relative VPS :", pos)
    print()

    start = max(0, pos - 64)

    data = payload[start:pos + 64]

    for i in range(0, len(data), 16):

        absolute = start + i

        chunk = data[i:i+16]

        hexs = " ".join(f"{b:02X}" for b in chunk)

        marker = ""

        if absolute == pos:

            marker = " <<< VPS"

        print(f"{absolute:08X}  {hexs:<47}{marker}")