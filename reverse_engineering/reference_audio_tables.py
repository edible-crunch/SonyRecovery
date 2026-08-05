from parsers.track_locator import get_tracks
from parsers.stco_reader import read_stco
from parsers.stsc_reader import read_stsc
from parsers.stsz_reader import read_stsz

REFERENCE = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)

tracks = get_tracks(REFERENCE)

audio = None

for track in tracks:

    with open(REFERENCE, "rb") as f:

        f.seek(track["hdlr"].offset + 16)

        handler = f.read(4).decode(errors="ignore")

    if handler == "soun":

        audio = track
        break

if audio is None:

    raise Exception("Audio track not found.")

stco = read_stco(
    REFERENCE,
    audio["stco"].offset
)

stsc = read_stsc(
    REFERENCE,
    audio["stsc"].offset
)

stsz = read_stsz(
    REFERENCE,
    audio["stsz"].offset
)

print()
print("=" * 70)
print("AUDIO TABLES")
print("=" * 70)

print()

print("STCO entries :", len(stco.offsets))

print("STSC entries :", len(stsc))

print("STSZ samples :", len(stsz))

print()

print("STSC")

for entry in stsc:

    print(entry)

print()

print("First 20 STCO")

for offset in stco.offsets[:20]:

    print(offset)

print()

print("First 20 STSZ")

for size in stsz[:20]:

    print(size)