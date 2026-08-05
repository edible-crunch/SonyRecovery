FILES = [
    (
        "Recovered",
        r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4",
    ),
    (
        "Candidate",
        "candidate_clip3.mp4",
    ),
]

OFFSET = 1298432

for name, path in FILES:

    print("=" * 60)
    print(name)
    print("=" * 60)

    with open(path, "rb") as f:
        f.seek(OFFSET)
        data = f.read(64)

    for i in range(0, len(data), 16):
        row = data[i:i+16]
        print(f"{i:04X}  " + " ".join(f"{b:02X}" for b in row))

    print()