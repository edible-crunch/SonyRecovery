from parsers.video_tables import get_video_tables

REFERENCE = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)

tables = get_video_tables(REFERENCE)

stco = tables["stco"].offsets
stsc = tables["stsc"]
stsz = tables["stsz"]

print("=" * 70)
print("REFERENCE CHUNK ANALYZER")
print("=" * 70)

print()

print("Video samples :", len(stsz))
print("Video chunks  :", len(stco))

print()

print("STSC entries:")
for e in stsc:
    print(e)

print()

first_chunk, samples_per_chunk, desc = stsc[0]

print("Samples per chunk:", samples_per_chunk)

print()

sample = 0

for chunk in range(min(10, len(stco))):

    first = sample
    last = sample + samples_per_chunk - 1

    size = sum(stsz[first:last+1])

    print(
        f"Chunk {chunk+1:03d} | "
        f"Offset={stco[chunk]:,} | "
        f"Samples={first+1}-{last+1} | "
        f"Bytes={size:,}"
    )

    sample += samples_per_chunk

print()

print("Total samples represented:", sample)