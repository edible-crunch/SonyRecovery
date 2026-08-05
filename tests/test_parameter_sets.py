from repair.hvcc import parse_hvcc
from parsers.mdat_reader import locate_mdat


def search(data, pattern):

    matches = []

    pos = 0

    while True:

        i = data.find(pattern, pos)

        if i == -1:
            break

        matches.append(i)

        pos = i + 1

    return matches


mp4 = input("Healthy MP4:\n").strip('"')

hvcc_file = input("HVCC BIN:\n").strip('"')

mdat = locate_mdat(mp4)

hvcc = parse_hvcc(hvcc_file)

print()
print("=" * 60)
print("READING MDAT")
print("=" * 60)

with open(mp4, "rb") as f:

    f.seek(mdat.data_offset)

    data = f.read(mdat.size)

print(f"Read {len(data):,} bytes")
print()

for array in hvcc.arrays:

    nal_type = array["type"]

    print("=" * 60)
    print(f"NAL TYPE {nal_type}")
    print("=" * 60)

    for index, nal in enumerate(array["nalus"], 1):

        print(f"NAL {index}")
        print(f"Length : {len(nal)}")

        matches = search(data, nal)

        print(f"Matches: {len(matches)}")

        if matches:

            print("First offsets:")

            for m in matches[:10]:

                print(f"  {m:,}")

        print()