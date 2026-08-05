import struct


def map_structure(data, center, before=128, after=256):

    start = max(0, center - before)
    end = min(len(data), center + after)

    print()
    print("=" * 80)
    print("STRUCTURE MAP")
    print("=" * 80)
    print()

    print(f"Center : {center:,}")
    print(f"Window : {start:,} -> {end:,}")
    print()

    p = start

    while p + 4 <= end:

        dword_be = struct.unpack(">I", data[p:p+4])[0]
        dword_le = struct.unpack("<I", data[p:p+4])[0]

        word_be = struct.unpack(">H", data[p:p+2])[0]
        word_le = struct.unpack("<H", data[p:p+2])[0]

        hexs = " ".join(f"{b:02X}" for b in data[p:p+16])

        text = "".join(
            chr(b) if 32 <= b < 127 else "."
            for b in data[p:p+16]
        )

        marker = ""

        if p == center:
            marker = "<-- MATCH"

        print(
            f"{p:08X}  "
            f"BE:{dword_be:10d} "
            f"LE:{dword_le:10d} "
            f"WBE:{word_be:5d} "
            f"WLE:{word_le:5d} "
            f"{marker}"
        )

        print(f"           {hexs}")
        print(f"           {text}")
        print()

        p += 4