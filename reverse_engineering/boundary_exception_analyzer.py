from parsers.video_tables import get_video_tables

RECOVERED_MOV = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mov\MOV_01m54s_000003.MOV"
)

CHUNK_STARTS = "chunk_starts.txt"

# ------------------------------------------------------------
# Load MOV tables
# ------------------------------------------------------------

tables = get_video_tables(RECOVERED_MOV)

stco = tables["stco"].offsets
stsc = tables["stsc"]
stsz = tables["stsz"]

samples_per_chunk = stsc[0][1]

# ------------------------------------------------------------
# Load detector hits
# ------------------------------------------------------------

detected = []

with open(CHUNK_STARTS) as f:

    for line in f:

        line = line.strip()

        if line:

            detected.append(int(line))

# ------------------------------------------------------------
# Build chunk boundaries
# ------------------------------------------------------------

chunk_bounds = []

sample_index = 0

for chunk_start in stco:

    chunk_size = sum(
        stsz[
            sample_index:
            sample_index + samples_per_chunk
        ]
    )

    chunk_end = chunk_start + chunk_size

    chunk_bounds.append(
        (chunk_start, chunk_end)
    )

    sample_index += samples_per_chunk

# ------------------------------------------------------------
# Investigate only the exceptions
# ------------------------------------------------------------

exceptions = [33, 95, 99]

print()
print("=" * 100)
print("BOUNDARY EXCEPTION ANALYZER")
print("=" * 100)

for chunk_number in exceptions:

    idx = chunk_number - 1

    detector = detected[idx]

    current_start, current_end = chunk_bounds[idx]

    prev_start = prev_end = None

    if idx > 0:
        prev_start, prev_end = chunk_bounds[idx - 1]

    print()
    print("-" * 100)
    print(f"Chunk {chunk_number}")
    print("-" * 100)

    print(f"Detector           : {detector:,}")
    print()

    if prev_start is not None:

        print(f"Previous Chunk")
        print(f"  Start            : {prev_start:,}")
        print(f"  End              : {prev_end:,}")
        print(f"  Distance to End  : {detector - prev_end:+,}")
        print()

    print(f"Current Chunk")
    print(f"  Start            : {current_start:,}")
    print(f"  End              : {current_end:,}")
    print(f"  Distance to Start: {detector - current_start:+,}")
    print(f"  Distance to End  : {detector - current_end:+,}")

    if prev_end is not None:
        if prev_start <= detector < prev_end:
            print()
            print("RESULT : Detector is INSIDE PREVIOUS chunk")

        elif current_start <= detector < current_end:
            print()
            print("RESULT : Detector is INSIDE CURRENT chunk")

        else:
            print()
            print("RESULT : Detector is OUTSIDE BOTH chunks")

print()
print("=" * 100)
print("DONE")
print("=" * 100)