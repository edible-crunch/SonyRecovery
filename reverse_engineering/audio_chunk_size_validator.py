from parsers.track_locator import get_tracks
from parsers.stco_reader import read_stco
from parsers.stsc_reader import read_stsc
from parsers.stsz_reader import read_stsz

REFERENCE = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)

# ------------------------------------------------------
# Locate tracks
# ------------------------------------------------------

tracks = get_tracks(REFERENCE)

video = None
audio = None

with open(REFERENCE, "rb") as f:

    for track in tracks:

        f.seek(track["hdlr"].offset + 16)
        handler = f.read(4).decode(errors="ignore")

        if handler == "vide":
            video = track

        elif handler == "soun":
            audio = track

if video is None:
    raise Exception("Video track not found.")

if audio is None:
    raise Exception("Audio track not found.")

# ------------------------------------------------------
# Read tables
# ------------------------------------------------------

video_stco = read_stco(
    REFERENCE,
    video["stco"].offset
)

video_stsc = read_stsc(
    REFERENCE,
    video["stsc"].offset
)

video_stsz = read_stsz(
    REFERENCE,
    video["stsz"].offset
)

audio_stco = read_stco(
    REFERENCE,
    audio["stco"].offset
)

audio_stsc = read_stsc(
    REFERENCE,
    audio["stsc"].offset
)

audio_stsz = read_stsz(
    REFERENCE,
    audio["stsz"].offset
)

video_samples_per_chunk = video_stsc[0][1]
audio_samples_per_chunk = audio_stsc[0][1]

print()
print("=" * 100)
print("AUDIO CHUNK SIZE VALIDATOR")
print("=" * 100)

video_sample = 0
audio_sample = 0

video_ok = True
audio_ok = True
equation_ok = True

video_diffs = []
audio_diffs = []
equation_diffs = []

chunks = min(
    len(video_stco.offsets) - 1,
    len(audio_stco.offsets) - 1
)

for i in range(chunks):

    video_bytes = sum(
        video_stsz[
            video_sample:
            video_sample + video_samples_per_chunk
        ]
    )

    audio_bytes = sum(
        audio_stsz[
            audio_sample:
            audio_sample + audio_samples_per_chunk
        ]
    )

    video_spacing = (
        video_stco.offsets[i + 1]
        - video_stco.offsets[i]
    )

    audio_spacing = (
        audio_stco.offsets[i + 1]
        - audio_stco.offsets[i]
    )

    video_diff = video_spacing - video_bytes
    audio_diff = audio_spacing - audio_bytes

    equation = (
        video_bytes + audio_bytes
    )

    equation_diff = video_spacing - equation

    video_diffs.append(video_diff)
    audio_diffs.append(audio_diff)
    equation_diffs.append(equation_diff)

    if video_diff != 0:
        video_ok = False

    if audio_diff != 0:
        audio_ok = False

    if equation_diff != 0:
        equation_ok = False

    if i < 10:

        print(
            f"{i+1:03d}"
        )

        print(
            f"  Video spacing : {video_spacing:,}"
        )

        print(
            f"  Video bytes   : {video_bytes:,}"
        )

        print(
            f"  Audio spacing : {audio_spacing:,}"
        )

        print(
            f"  Audio bytes   : {audio_bytes:,}"
        )

        print(
            f"  Equation diff : {equation_diff:+,}"
        )

        print()

    video_sample += video_samples_per_chunk
    audio_sample += audio_samples_per_chunk

print("=" * 100)
print("SUMMARY")
print("=" * 100)

print()

print("VIDEO")
print(f"Min : {min(video_diffs):+,}")
print(f"Max : {max(video_diffs):+,}")

print()

print("AUDIO")
print(f"Min : {min(audio_diffs):+,}")
print(f"Max : {max(audio_diffs):+,}")

print()

print("VIDEO + AUDIO EQUATION")
print(f"Min : {min(equation_diffs):+,}")
print(f"Max : {max(equation_diffs):+,}")

print()

if equation_ok:

    print("RESULT : Video spacing equals Video bytes + Audio bytes.")

else:

    print("RESULT : Additional data still exists.")