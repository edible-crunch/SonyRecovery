from parsers.stsc_reader import read_stsc
from parsers.stsz_reader import read_stsz
from parsers.track_locator import get_tracks

REFERENCE = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)

META_PAYLOAD = 1_167_360
AUDIO_PAYLOAD = 192_192

tracks = get_tracks(REFERENCE)

video = None

with open(REFERENCE, "rb") as f:
    for track in tracks:
        f.seek(track["hdlr"].offset + 16)
        if f.read(4).decode(errors="ignore") == "vide":
            video = track
            break

stsc = read_stsc(
    REFERENCE,
    video["stsc"].offset
)

stsz = read_stsz(
    REFERENCE,
    video["stsz"].offset
)

samples_per_chunk = stsc[0][1]

video_sample = 0

meta_offset = 0

layout = []

while video_sample < len(stsz):

    video_payload = sum(
        stsz[
            video_sample:
            video_sample + samples_per_chunk
        ]
    )

    video_offset = meta_offset + META_PAYLOAD

    audio_offset = video_offset + video_payload

    layout.append(
        {
            "meta": meta_offset,
            "video": video_offset,
            "audio": audio_offset,
            "video_payload": video_payload,
        }
    )

    meta_offset = audio_offset + AUDIO_PAYLOAD

    video_sample += samples_per_chunk

print()
print("=" * 90)
print("LAYOUT GENERATOR")
print("=" * 90)

for i, c in enumerate(layout[:10]):

    print()

    print(f"Chunk {i+1}")

    print(f"Meta  : {c['meta']:,}")
    print(f"Video : {c['video']:,}")
    print(f"Audio : {c['audio']:,}")

    print(f"Video payload : {c['video_payload']:,}")

print()

print(f"Chunks generated : {len(layout)}")