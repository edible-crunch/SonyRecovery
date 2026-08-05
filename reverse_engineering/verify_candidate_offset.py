START = 1429504

FILE = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

with open(FILE, "rb") as f:
    f.seek(START)
    data = f.read(32)

print("Offset:", START)
print()

for i in range(0, len(data), 16):

    row = data[i:i+16]

    print(
        f"{START+i:08X}  " +
        " ".join(f"{b:02X}" for b in row)
    )

length = int.from_bytes(data[:4], "big")

print()
print("Length:", length)
print("NAL header:", hex(data[4]))