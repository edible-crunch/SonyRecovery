from parsers.mdat_reader import locate_mdat


RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

CANDIDATE_MP4 = "candidate_clip3.mp4"

# First video chunk from STCO
FIRST_CHUNK_OFFSET = 1298432

# Number of bytes to compare
NUM_BYTES = 64


def read_bytes(filename):

    mdat = locate_mdat(filename)

    with open(filename, "rb") as f:

        f.seek(FIRST_CHUNK_OFFSET)

        return f.read(NUM_BYTES)


def dump(title, data):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    for i in range(0, len(data), 16):

        row = data[i:i+16]

        hexs = " ".join(f"{b:02X}" for b in row)

        print(f"{i:04X}  {hexs}")


a = read_bytes(RECOVERED_MP4)
b = read_bytes(CANDIDATE_MP4)

dump("Recovered MP4", a)
dump("Candidate MP4", b)

print()
print("=" * 60)

if a == b:
    print("IDENTICAL")
else:
    print("DIFFERENT")

    for i in range(min(len(a), len(b))):

        if a[i] != b[i]:

            print()
            print(f"First difference at byte {i}")
            print(f"Recovered : {a[i]:02X}")
            print(f"Candidate : {b[i]:02X}")

            break