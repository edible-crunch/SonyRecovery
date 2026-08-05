from parsers.video_tables import get_video_tables

HEALTHY = r"C:\Users\johne\OneDrive\Desktop\ENABLE\C0946.MP4"

tables = get_video_tables(HEALTHY)

sizes = tables["stsz"]

print("=" * 70)
print("HEALTHY STSZ")
print("=" * 70)

print("Frames :", len(sizes))
print()

print("First 20 frame sizes:")

for s in sizes[:20]:
    print(s)

with open("healthy_stsz.txt", "w") as f:

    for s in sizes:
        f.write(f"{s}\n")

print()
print("[OK] healthy_stsz.txt written.")