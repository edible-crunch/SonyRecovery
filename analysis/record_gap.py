import struct


def inspect_gap(data, start1, length1, start2):

    end1 = start1 + 8 + length1

    gap_start = end1
    gap_end = start2

    print()
    print("=" * 80)
    print("RECORD GAP")
    print("=" * 80)

    print()
    print(f"Record 1 Start : {start1:,}")
    print(f"Record 1 End   : {end1:,}")

    print(f"Record 2 Start : {start2:,}")

    print()

    gap = data[gap_start:gap_end]

    print(f"Gap Length : {len(gap)} bytes")
    print()

    if len(gap) == 0:

        print("No gap.")
        return

    print("Hex")

    print()

    for i in range(0, len(gap), 16):

        chunk = gap[i:i+16]

        hexs = " ".join(
            f"{b:02X}" for b in chunk
        )

        text = "".join(
            chr(b) if 32 <= b < 127 else "."
            for b in chunk
        )

        print(
            f"{gap_start+i:08X}  "
            f"{hexs:<47} "
            f"{text}"
        )

    print()

    print("DWORD interpretations")

    print()

    for i in range(0, len(gap)-3):

        value_le = struct.unpack(
            "<I",
            gap[i:i+4]
        )[0]

        value_be = struct.unpack(
            ">I",
            gap[i:i+4]
        )[0]

        print(
            f"+{i:02d}  "
            f"LE={value_le:<10} "
            f"BE={value_be:<10}"
        )