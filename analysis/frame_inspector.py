def inspect_frame(filename, bytes_to_show=128):

    with open(filename, "rb") as f:

        data = f.read(bytes_to_show)

    print()
    print("First", len(data), "bytes")
    print("-" * 60)

    for i in range(0, len(data), 16):

        chunk = data[i:i+16]

        hex_bytes = " ".join(f"{b:02X}" for b in chunk)

        ascii_bytes = "".join(
            chr(b) if 32 <= b <= 126 else "."
            for b in chunk
        )

        print(f"{i:04X}  {hex_bytes:<47}  {ascii_bytes}")

    print()

    if len(data) >= 4:

        nal_length = int.from_bytes(data[:4], "big")

        print("First NAL Length:", nal_length)

    if len(data) >= 5:

        nal_header = data[4]

        nal_type = (nal_header >> 1) & 0x3F

        print("Possible HEVC NAL Type:", nal_type)