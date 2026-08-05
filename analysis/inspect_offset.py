def dump(f, offset, count=128):

    f.seek(offset)
    data = f.read(count)

    print(f"\nOffset {offset} (0x{offset:X})")
    print("-" * 60)

    for i in range(0, len(data), 16):
        chunk = data[i:i+16]

        hexs = " ".join(f"{b:02X}" for b in chunk)
        text = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)

        print(f"{offset+i:08X}  {hexs:<47} {text}")


file = input("Drag recovered MP4 here:\n").strip().strip('"')

with open(file, "rb") as f:

    dump(f, 131072)
    dump(f, 1298432)