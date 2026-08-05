def scan_start_codes(filename):

    with open(filename, "rb") as f:
        data = f.read()

    print()
    print("Searching for Annex B start codes...")
    print("-" * 60)

    found = 0

    i = 0

    while i < len(data) - 4:

        # 00 00 01
        if data[i:i+3] == b"\x00\x00\x01":
            print(f"3-byte start code at {i:,}")
            found += 1
            i += 3
            continue

        # 00 00 00 01
        if data[i:i+4] == b"\x00\x00\x00\x01":
            print(f"4-byte start code at {i:,}")
            found += 1
            i += 4
            continue

        i += 1

    print()
    print("Total start codes found:", found)