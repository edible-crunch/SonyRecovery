import os

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

with open("chunk_starts.txt") as f:
    starts = [int(x.strip()) for x in f if x.strip()]

filesize = os.path.getsize(RECOVERED_MP4)

print("=" * 60)
print("LAST CHUNK")
print("=" * 60)

print("File size :", filesize)
print("Last GOP  :", starts[-1])

print()
print("Remaining bytes:")
print(filesize - starts[-1])