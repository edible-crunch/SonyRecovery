PATTERN = bytes.fromhex(
    "00000003460110000000164E01"
)

FILE = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

with open(FILE, "rb") as f:
    data = f.read()

matches = []

start = 0

while True:
    pos = data.find(PATTERN, start)

    if pos == -1:
        break

    matches.append(pos)
    start = pos + 1

print("Matches:", len(matches))

for m in matches[:20]:
    print(m)