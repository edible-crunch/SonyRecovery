from parsers.track_locator import get_tracks
from parsers.stco_reader import read_stco
from parsers.stsc_reader import read_stsc
from parsers.stsz_reader import read_stsz

REFERENCE = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)

# -------------------------------------------------------
# Locate video track
# -------------------------------------------------------

tracks = get_tracks(REFERENCE)

video = None

for track in tracks:

    with open(REFERENCE, "rb") as f:

        f.seek(track["hdlr"].offset + 16)

        if f.read(4).decode(errors="ignore") == "vide":

            video = track
            break

if video is None:
    raise Exception("Video track not found.")

# -------------------------------------------------------
# Read tables
# -------------------------------------------------------

stco = read_stco(
    REFERENCE,
    video["stco"].offset
)

stsc = read_stsc(
    REFERENCE,
    video["stsc"].offset
)

stsz = read_stsz(
    REFERENCE,
    video["stsz"].offset
)

samples_per_chunk = stsc[0][1]

print()
print("=" * 100)
print("CHUNK SPACING VALIDATOR")
print("=" * 100)

sample_index = 0

all_zero = True

differences = []

for chunk in range(len(stco.offsets) - 1):

    measured_spacing = (
        stco.offsets[chunk + 1]
        - stco.offsets[chunk]
    )

    sample_total = sum(
        stsz[
            sample_index:
            sample_index + samples_per_chunk
        ]
    )

    difference = measured_spacing - sample_total

    differences.append(difference)

    if difference != 0:
        all_zero = False

    print(
        f"{chunk+1:03d}  "
        f"Measured={measured_spacing:,}  "
        f"Samples={sample_total:,}  "
        f"Difference={difference:+,}"
    )

    sample_index += samples_per_chunk

print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)

print(f"Chunks tested : {len(differences)}")

print(f"Min difference: {min(differences):+,}")

print(f"Max difference: {max(differences):+,}")

average = sum(differences) / len(differences)

print(f"Average       : {average:,.1f}")

print()

if all_zero:

    print("RESULT : Chunk spacing exactly equals STSZ totals.")

else:

    print("RESULT : Chunk spacing differs from STSZ totals.")