from recovery.chunk_parser import parse_chunk
from recovery.access_unit_parser import split_access_units

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

START = 1560576
END = 22460249

chunk = parse_chunk(
    RECOVERED_MP4,
    START,
    END
)

frames = split_access_units(chunk)

print("=" * 70)
print("ACCESS UNIT PARSER")
print("=" * 70)

print("Frames found:", len(frames))
print()

for i, frame in enumerate(frames[:15]):

    print(
        f"Frame {i+1:02d}"
    )

    print(
        f"Offset : {frame['offset']:,}"
    )

    print(
        f"Size   : {frame['size']:,}"
    )

    print(
        "NALs:"
    )

    for nal in frame["nals"]:

        print(
            f"   {nal['name']:<12}"
            f"{nal['length']:,}"
        )

    print()