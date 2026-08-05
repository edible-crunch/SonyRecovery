def nal_type(byte):

    return (byte >> 1) & 0x3F


file = input("Drag frame_000001.bin here:\n").strip().strip('"')

with open(file, "rb") as f:
    data = f.read()

print()
print("Scanning...")
print()

found = 0

i = 0

while i < len(data) - 4:

    # 4-byte Annex B start code
    if data[i:i+4] == b"\x00\x00\x00\x01":

        if i + 4 < len(data):

            header = data[i+4]
            ntype = nal_type(header)

            print(
                f"Offset {i:8} (0x{i:08X}) "
                f"StartCode=00000001 "
                f"NAL={ntype:2} "
                f"Header=0x{header:02X}"
            )

            found += 1

        i += 4
        continue

    # 3-byte Annex B start code
    if data[i:i+3] == b"\x00\x00\x01":

        if i + 3 < len(data):

            header = data[i+3]
            ntype = nal_type(header)

            print(
                f"Offset {i:8} (0x{i:08X}) "
                f"StartCode=000001 "
                f"NAL={ntype:2} "
                f"Header=0x{header:02X}"
            )

            found += 1

        i += 3
        continue

    i += 1

print()
print("Total start codes found:", found)