from repair.hvcc import parse_hvcc
from parsers.mdat_reader import locate_mdat


BEFORE = 64
AFTER = 256


def hexdump(data, base_offset):

    for i in range(0, len(data), 16):

        chunk = data[i:i + 16]

        hexs = " ".join(f"{b:02X}" for b in chunk)

        text = "".join(
            chr(b) if 32 <= b < 127 else "."
            for b in chunk
        )

        print(
            f"{base_offset + i:08X}  "
            f"{hexs:<47} "
            f"{text}"
        )


def find_all(data, pattern):

    pos = 0

    while True:

        idx = data.find(pattern, pos)

        if idx == -1:
            return

        yield idx

        pos = idx + 1


mp4 = input("MP4:\n").strip('"')
hvcc_file = input("HVCC BIN:\n").strip('"')

mdat = locate_mdat(mp4)
hvcc = parse_hvcc(hvcc_file)

print()
print("=" * 60)
print("READING MDAT")
print("=" * 60)

with open(mp4, "rb") as f:

    f.seek(mdat.data_offset)

    payload = f.read(mdat.size)

print(f"Payload size : {len(payload):,}")
print()

for array in hvcc.arrays:

    print("=" * 60)
    print(f"NAL TYPE {array['type']}")
    print("=" * 60)

    for nal_index, nal in enumerate(array["nalus"], 1):

        print()
        print(f"NAL {nal_index}")
        print(f"Length : {len(nal)}")

        matches = list(find_all(payload, nal))

        print(f"Matches: {len(matches)}")

        for match_no, offset in enumerate(matches, 1):

            print()
            print("-" * 60)
            print(f"Match {match_no}")
            print(f"Payload Offset : {offset:,}")
            print(f"Absolute File  : {mdat.data_offset + offset:,}")

            start = max(0, offset - BEFORE)
            end = min(len(payload), offset + len(nal) + AFTER)

            print()
            print("Hex dump")
            print()

            hexdump(
                payload[start:end],
                start
            )