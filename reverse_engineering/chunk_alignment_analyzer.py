from parsers.video_tables import get_video_tables
from parsers.stsz_reader import read_stsz

RECOVERED_MOV = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mov\MOV_01m54s_000003.MOV"
)

CHUNK_STARTS = "chunk_starts.txt"

tables = get_video_tables(RECOVERED_MOV)

stco = tables["stco"].offsets
stsc = tables["stsc"]
stsz = tables["stsz"]

# Healthy Sony model:
# one STSC entry
# 60 samples per chunk

samples_per_chunk = stsc[0][1]

# ------------------------------------------------------
# detected signatures
# ------------------------------------------------------

detected = []

with open(CHUNK_STARTS) as f:

    for line in f:

        line = line.strip()

        if line:

            detected.append(int(line))

print()
print("=" * 100)
print("CHUNK ALIGNMENT ANALYZER")
print("=" * 100)

sample_index = 0

inside_count = 0
outside_count = 0

for chunk in range(len(stco)):

    chunk_start = stco[chunk]

    chunk_size = sum(
        stsz[
            sample_index:
            sample_index + samples_per_chunk
        ]
    )

    chunk_end = chunk_start + chunk_size

    detector = detected[chunk]

    inside = (
        chunk_start <= detector < chunk_end
    )

    if inside:
        inside_count += 1
    else:
        outside_count += 1

    distance = detector - chunk_start

    print(
        f"{chunk+1:03d}  "
        f"Chunk=[{chunk_start:,} .. {chunk_end:,})  "
        f"Detector={detector:,}  "
        f"Distance={distance:+,}  "
        f"{'INSIDE' if inside else 'OUTSIDE'}"
    )

    sample_index += samples_per_chunk

print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)

print("Inside :", inside_count)
print("Outside:", outside_count)