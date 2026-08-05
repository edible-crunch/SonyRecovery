from parsers.video_tables import get_video_tables

RECOVERED_MOV = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mov\MOV_01m54s_000003.MOV"
)

CHUNK_STARTS = "chunk_starts.txt"

# ----------------------------------------------------------
# Load tables
# ----------------------------------------------------------

tables = get_video_tables(RECOVERED_MOV)

stsz = tables["stsz"]
stsc = tables["stsc"]

samples_per_chunk = stsc[0][1]

# ----------------------------------------------------------
# Load detector hits
# ----------------------------------------------------------

detected = []

with open(CHUNK_STARTS) as f:
    for line in f:
        line = line.strip()
        if line:
            detected.append(int(line))

print()
print("=" * 80)
print("ANCHOR SOLVER")
print("=" * 80)

print(f"Detected chunk markers : {len(detected)}")
print(f"Video samples          : {len(stsz)}")

# ----------------------------------------------------------
# Compute chunk sizes from STSZ/STSC
# ----------------------------------------------------------

chunk_sizes = []

sample = 0

while sample + samples_per_chunk <= len(stsz):

    size = sum(
        stsz[
            sample:
            sample + samples_per_chunk
        ]
    )

    chunk_sizes.append(size)

    sample += samples_per_chunk

print(f"Computed chunk sizes   : {len(chunk_sizes)}")

# ----------------------------------------------------------
# Try every possible detector alignment
# ----------------------------------------------------------

best = None

for detector_shift in range(len(detected) - len(chunk_sizes) + 1):

    # Assume first computed chunk starts at:
    anchor = detected[detector_shift]

    calculated = [anchor]

    for size in chunk_sizes[:-1]:
        calculated.append(
            calculated[-1] + size
        )

    errors = []

    for i in range(len(chunk_sizes)):

        det = detected[i + detector_shift]
        calc = calculated[i]

        errors.append(det - calc)

    mean_error = sum(abs(e) for e in errors) / len(errors)
    max_error = max(abs(e) for e in errors)

    if (
        best is None
        or mean_error < best["mean"]
    ):
        best = {
            "shift": detector_shift,
            "anchor": anchor,
            "mean": mean_error,
            "max": max_error,
            "errors": errors,
        }

print()
print("=" * 80)
print("BEST FIT")
print("=" * 80)

print(f"Detector shift : {best['shift']}")
print(f"Anchor         : {best['anchor']:,}")
print(f"Mean error     : {best['mean']:.1f} bytes")
print(f"Max error      : {best['max']:,} bytes")

print()
print("First 20 errors")

for e in best["errors"][:20]:
    print(e)