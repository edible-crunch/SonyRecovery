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

for track in tracks:

    with open(REFERENCE, "rb") as f:

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

# -------------------------------------------------------
# Read tables
# -------------------------------------------------------

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

# -------------------------------------------------------
# We already know the healthy STSC has one entry.
# -------------------------------------------------------

samples_per_chunk = video_stsc[0][1]

print()
print("=" * 80)
print("VIDEO / AUDIO INTERLEAVE CHECK")
print("=" * 80)

sample_index = 0

all_zero = True

for chunk_index in range(len(video_stco.offsets)):

    start = sample_index
    end = start + samples_per_chunk

    video_size = sum(
        video_stsz[start:end]
    )

    video_offset = video_stco.offsets[chunk_index]

    expected_audio = video_offset + video_size

    actual_audio = audio_stco.offsets[chunk_index]

    difference = actual_audio - expected_audio

    if difference != 0:
        all_zero = False

    print(
        f"Chunk {chunk_index+1:03d}"
    )

    print(
        f"  Video Offset   : {video_offset:,}"
    )

    print(
        f"  Video Size     : {video_size:,}"
    )

    print(
        f"  Expected Audio : {expected_audio:,}"
    )

    print(
        f"  Actual Audio   : {actual_audio:,}"
    )

    print(
        f"  Difference     : {difference:+,}"
    )

    print()

    sample_index += samples_per_chunk

print("=" * 80)

if all_zero:

    print("SUCCESS")
    print("Every audio chunk begins immediately after its video chunk.")

else:

    print("Differences detected.")
    print("Sony is inserting padding or using another interleave pattern.")