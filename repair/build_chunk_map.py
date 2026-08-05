PATTERN = bytes.fromhex(
    "00000003460110000000164E01"
)

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

CHUNK_SIZE = 16 * 1024 * 1024

matches = []

print("=" * 70)
print("BUILDING CHUNK MAP")
print("=" * 70)

with open(RECOVERED_MP4, "rb") as f:

    file_offset = 0
    overlap = len(PATTERN) - 1
    previous = b""

    while True:

        chunk = f.read(CHUNK_SIZE)

        if not chunk:
            break

        data = previous + chunk

        start = 0

        while True:

            pos = data.find(PATTERN, start)

            if pos == -1:
                break

            absolute = file_offset - len(previous) + pos

            matches.append(absolute)

            start = pos + 1

        previous = data[-overlap:]
        file_offset += len(chunk)

print()
print(f"Verified GOP starts : {len(matches)}")
print()

print("=" * 70)
print("CHUNK MAP")
print("=" * 70)

total = 0
largest = 0
smallest = None

for i in range(len(matches) - 1):

    start = matches[i]
    end = matches[i + 1]

    size = end - start

    total += size

    if size > largest:
        largest = size

    if smallest is None or size < smallest:
        smallest = size

    print(
        f"{i+1:03d}  "
        f"{start:,}  ->  "
        f"{end:,}   "
        f"Size = {size:,}"
    )

average = total / (len(matches) - 1)

print()
print("=" * 70)
print("STATISTICS")
print("=" * 70)

print(f"Chunks     : {len(matches)-1}")
print(f"Average    : {average:,.1f}")
print(f"Smallest   : {smallest:,}")
print(f"Largest    : {largest:,}")

print()
print("First 10 GOP starts:")

for m in matches[:10]:
    print(m)

with open("chunk_starts.txt", "w") as f:
    for start in matches:
        f.write(f"{start}\n")

print()
print("[OK] chunk_starts.txt written.")