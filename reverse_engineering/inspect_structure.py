from repair.hvcc import parse_hvcc
from parsers.mdat_reader import locate_mdat
from analysis.structure_mapper import map_structure


def find_first(data, pattern):

    return data.find(pattern)


mp4 = input("MP4:\n").strip('"')
hvcc = input("HVCC:\n").strip('"')

mdat = locate_mdat(mp4)
cfg = parse_hvcc(hvcc)

with open(mp4, "rb") as f:

    f.seek(mdat.data_offset)

    payload = f.read(mdat.size)

for array in cfg.arrays:

    for nal in array["nalus"]:

        pos = find_first(payload, nal)

        if pos == -1:
            continue

        print()
        print("=" * 80)
        print(f"NAL TYPE {array['type']}")
        print("=" * 80)

        map_structure(payload, pos)

        break