def hex_dump(filename, offset, count=128):

    with open(filename, "rb") as f:

        f.seek(offset)

        data = f.read(count)

    print()
    print(f"Offset: {offset}")
    print("-" * 75)

    for i in range(0, len(data), 16):

        chunk = data[i:i+16]

        hex_bytes = " ".join(f"{b:02X}" for b in chunk)

        ascii_bytes = "".join(
            chr(b) if 32 <= b <= 126 else "."
            for b in chunk
        )

        print(f"{offset+i:08X}  {hex_bytes:<47}  {ascii_bytes}")