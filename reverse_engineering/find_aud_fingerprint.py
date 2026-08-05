PATTERN = bytes.fromhex(
    "00000003460110000000164E01"
)

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

CHUNK_SIZE = 16 * 1024 * 1024

print("=" * 70)
print("SEARCHING FOR SONY AUD FINGERPRINT")
print("=" * 70)
print()

matches = []

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

            print(f"Match at file offset : {absolute:,}")

            start = pos + 1

        previous = data[-overlap:]
        file_offset += len(chunk)

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Matches found : {len(matches)}")

if matches:
    print()
    print("First 20 matches:")

    for m in matches[:20]:
        print(f"{m:,}")