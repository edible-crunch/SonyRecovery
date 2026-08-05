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
# Locate tracks
# -------------------------------------------------------

tracks = get_tracks(REFERENCE)

video = None
audio = None
meta = None

with open(REFERENCE, "rb") as f:

    for track in tracks:

        f.seek(track["hdlr"].offset + 16)

        handler = f.read(4).decode(errors="ignore")

        if handler == "vide":
            video = track

        elif handler == "soun":
            audio = track

        elif handler == "meta":
            meta = track

# -------------------------------------------------------
# Read metadata tables
# -------------------------------------------------------

meta_stco = read_stco(
    REFERENCE,
    meta["stco"].offset
)

meta_stsc = read_stsc(
    REFERENCE,
    meta["stsc"].offset
)

meta_stsz = read_stsz(
    REFERENCE,
    meta["stsz"].offset
)

samples_per_chunk = meta_stsc[0][1]

print()
print("=" * 100)
print("META CHUNK SIZE VALIDATOR")
print("=" * 100)

sample_index = 0

payload_diffs = []

for i in range(len(meta_stco.offsets) - 1):

    payload_bytes = sum(
        meta_stsz[
            sample_index:
            sample_index + samples_per_chunk
        ]
    )

    spacing = (
        meta_stco.offsets[i + 1]
        - meta_stco.offsets[i]
    )

    difference = spacing - payload_bytes

    payload_diffs.append(difference)

    if i < 10:

        print(f"{i+1:03d}")

        print(f"  Meta spacing : {spacing:,}")
        print(f"  Meta payload : {payload_bytes:,}")
        print(f"  Difference   : {difference:+,}")

        print()

    sample_index += samples_per_chunk

print("=" * 100)
print("SUMMARY")
print("=" * 100)

print()

print(f"Chunks tested : {len(payload_diffs)}")

print(f"Minimum diff  : {min(payload_diffs):+,}")

print(f"Maximum diff  : {max(payload_diffs):+,}")

avg = sum(payload_diffs) / len(payload_diffs)

print(f"Average diff  : {avg:,.1f}")

print()

if min(payload_diffs) == max(payload_diffs):

    print("Difference is perfectly constant.")

else:

    print("Difference varies between chunks.")