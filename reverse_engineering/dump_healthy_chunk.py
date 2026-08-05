HEALTHY = r"C:\Users\johne\OneDrive\Desktop\ENABLE\C0946.MP4"

OFFSET = 1298432

with open(HEALTHY, "rb") as f:
    f.seek(OFFSET)
    data = f.read(64)

for i in range(0, len(data), 16):
    chunk = data[i:i+16]
    print(
        f"{OFFSET+i:08X}:",
        " ".join(f"{b:02X}" for b in chunk)
    )