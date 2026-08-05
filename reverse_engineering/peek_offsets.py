FILE = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

OFFSET = 1560576

with open(FILE, "rb") as f:

    f.seek(OFFSET)

    print("Tell :", f.tell())

    data = f.read(32)

print()

print("Bytes:")

print(" ".join(f"{b:02X}" for b in data))

print()

print("As hex:")

print(data.hex())