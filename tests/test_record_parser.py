from repair.hvcc import parse_hvcc
from parsers.mdat_reader import locate_mdat

from recovery.record_parser import parse_record


def find_first(data, pattern):

    return data.find(pattern)


mp4 = input("MP4:\n").strip('"')

hvcc = input("HVCC:\n").strip('"')

mdat = locate_mdat(mp4)

cfg = parse_hvcc(hvcc)

with open(mp4, "rb") as f:

    f.seek(mdat.data_offset)

    payload = f.read(mdat.size)

print()

for array in cfg.arrays:

    for nal in array["nalus"]:

        pos = find_first(payload, nal)

        if pos == -1:

            continue

        print("=" * 60)

        print(f"NAL TYPE {array['type']}")

        print("=" * 60)

        for back in range(0, 32):

            start = pos - back

            if start < 0:

                continue

            r = parse_record(payload, start)

            if r is None:

                continue

            print()

            print("Candidate")

            print("Backtrack :", back)

            print("Offset    :", start)

            print("Length    :", r.length)

            print("Tag       :", hex(r.tag))

            print("NAL       :", r.header["nal_name"])

        break