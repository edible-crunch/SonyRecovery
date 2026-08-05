from recovery.access_unit_parser import parse_access_units

FILE = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000001.MP4"

frames = parse_access_units(FILE)

print("="*60)
print("SUMMARY")
print("="*60)

print("Frames:", len(frames))

count = 0

for i, frame in enumerate(frames, 1):
    if i <= 10:
        print(
            i,
            frame["offset"],
            frame["size"]
        )

print()

sizes = [f["size"] for f in frames]

print("Average frame size:", sum(sizes)/len(sizes))
print("Largest:", max(sizes))
print("Smallest:", min(sizes))