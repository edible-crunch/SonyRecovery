from recovery.chunk_parser import parse_chunk

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

CHUNK_START = 1560576
CHUNK_END = 22460249

result = parse_chunk(
    RECOVERED_MP4,
    CHUNK_START,
    CHUNK_END
)

print("=" * 70)
print("CHUNK PARSER")
print("=" * 70)

print("Chunk size :", result["chunk_size"])
print("Bytes read :", result["bytes_consumed"])
print("NAL count  :", len(result["nals"]))

print()

for i, nal in enumerate(result["nals"][:100]):

    print(
        f"{i+1:03d}  "
        f"{nal['offset']:,}  "
        f"{nal['name']:<12}  "
        f"{nal['length']:,}"
    )