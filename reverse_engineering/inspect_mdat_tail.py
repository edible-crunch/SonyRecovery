from parsers.mdat_reader import locate_mdat


def hex_dump(data):

    for i in range(0, len(data), 16):

        chunk = data[i:i+16]

        hexs = " ".join(
            f"{b:02X}" for b in chunk
        )

        text = "".join(
            chr(b) if 32 <= b < 127 else "."
            for b in chunk
        )

        print(
            f"{i:08X}  "
            f"{hexs:<47} "
            f"{text}"
        )


mp4 = input("Recovered MP4:\n").strip('"')

mdat = locate_mdat(mp4)

print()
print("MDAT")
print("-" * 60)

print("Offset :", mdat.offset)
print("Payload:", mdat.data_offset)
print("Size   :", mdat.size)

TAIL_SIZE = 4096

with open(mp4, "rb") as f:

    start = mdat.data_offset + (mdat.size - 16) - TAIL_SIZE

    f.seek(start)

    data = f.read(TAIL_SIZE)

print()
print("Last 4096 bytes")
print("-" * 60)

hex_dump(data)