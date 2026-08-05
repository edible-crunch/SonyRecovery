from parsers.track_locator import get_tracks
from parsers.stco_reader import read_stco
from parsers.stsc_reader import read_stsc
from parsers.stsz_reader import read_stsz

REFERENCE = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)

# ----------------------------------------------------------
# Locate tracks
# ----------------------------------------------------------

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

if not all([video, audio, meta]):
    raise Exception("Could not locate all three tracks.")

# ----------------------------------------------------------
# Read tables
# ----------------------------------------------------------

video_stco = read_stco(REFERENCE, video["stco"].offset)
video_stsc = read_stsc(REFERENCE, video["stsc"].offset)
video_stsz = read_stsz(REFERENCE, video["stsz"].offset)

audio_stco = read_stco(REFERENCE, audio["stco"].offset)
audio_stsc = read_stsc(REFERENCE, audio["stsc"].offset)
audio_stsz = read_stsz(REFERENCE, audio["stsz"].offset)

meta_stco = read_stco(REFERENCE, meta["stco"].offset)
meta_stsc = read_stsc(REFERENCE, meta["stsc"].offset)
meta_stsz = read_stsz(REFERENCE, meta["stsz"].offset)

video_samples = video_stsc[0][1]
audio_samples = audio_stsc[0][1]
meta_samples = meta_stsc[0][1]

v_sample = 0
a_sample = 0
m_sample = 0

print()
print("=" * 100)
print("MUX CYCLE MAPPER")
print("=" * 100)

for i in range(10):

    video_payload = sum(
        video_stsz[
            v_sample:
            v_sample + video_samples
        ]
    )

    audio_payload = sum(
        audio_stsz[
            a_sample:
            a_sample + audio_samples
        ]
    )

    meta_payload = sum(
        meta_stsz[
            m_sample:
            m_sample + meta_samples
        ]
    )

    video_spacing = (
        video_stco.offsets[i + 1]
        - video_stco.offsets[i]
    )

    accounted = (
        audio_payload +
        meta_payload
    )

    remaining = (
        video_spacing -
        video_payload -
        accounted
    )

    print(f"\nCycle {i+1}")
    print("-" * 60)

    print(f"Meta  Offset : {meta_stco.offsets[i]:,}")
    print(f"Video Offset : {video_stco.offsets[i]:,}")
    print(f"Audio Offset : {audio_stco.offsets[i]:,}")

    print()

    print(f"Meta Payload : {meta_payload:,}")
    print(f"VideoPayload : {video_payload:,}")
    print(f"AudioPayload : {audio_payload:,}")

    print()

    print(f"Video→Video spacing : {video_spacing:,}")
    print(f"Accounted payload   : {video_payload + accounted:,}")
    print(f"Remaining bytes     : {remaining:+,}")

    v_sample += video_samples
    a_sample += audio_samples
    m_sample += meta_samples

print()
print("=" * 100)
print("DONE")
print("=" * 100)