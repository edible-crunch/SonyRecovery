def hex_dump(data, start=0, length=256):
    end = min(len(data), start + length)

    for offset in range(start, end, 16):
        chunk = data[offset:offset + 16]

        hex_bytes = " ".join(f"{b:02X}" for b in chunk)
        ascii_bytes = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)

        print(f"{offset:08X}  {hex_bytes:<47} {ascii_bytes}")


file = input("Drag recovered MP4 here:\n").strip().strip('"')

with open(file, "rb") as f:
    data = f.read(512)

print()
print("First 512 bytes")
print("-" * 70)

hex_dump(data)