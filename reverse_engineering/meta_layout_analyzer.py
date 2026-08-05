from parsers.track_locator import get_tracks
from parsers.stco_reader import read_stco

REFERENCE = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)

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

video_stco = read_stco(
    REFERENCE,
    video["stco"].offset
)

audio_stco = read_stco(
    REFERENCE,
    audio["stco"].offset
)

meta_stco = read_stco(
    REFERENCE,
    meta["stco"].offset
)

print()
print("=" * 90)
print("META LAYOUT ANALYZER")
print("=" * 90)

for i in range(10):

    print(f"\nChunk {i+1}")

    print(
        f"Video : {video_stco.offsets[i]:,}"
    )

    print(
        f"Audio : {audio_stco.offsets[i]:,}"
    )

    print(
        f"Meta  : {meta_stco.offsets[i]:,}"
    )

    print(
        f"Meta-Video : "
        f"{meta_stco.offsets[i]-video_stco.offsets[i]:+,}"
    )

    print(
        f"Meta-Audio : "
        f"{meta_stco.offsets[i]-audio_stco.offsets[i]:+,}"
    )