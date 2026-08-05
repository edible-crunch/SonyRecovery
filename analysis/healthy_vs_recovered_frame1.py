from parsers.video_tables import get_video_tables
from recovery.frame_mapper import build_frame_map

HEALTHY = r"C:\Users\johne\OneDrive\Desktop\ENABLE\C0946.MP4"

RECOVERED_MOV = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mov\MOV_01m54s_000003.MOV"

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"


def first_frame(filename):

    tables = get_video_tables(filename)

    frame_map = build_frame_map(
        tables["stco"].offsets,
        tables["stsc"],
        tables["stsz"]
    )

    return frame_map[0]


healthy = first_frame(HEALTHY)
recovered = first_frame(RECOVERED_MOV)


def read_sample(filename, frame):

    with open(filename, "rb") as f:

        f.seek(frame["offset"])

        return f.read(256)


healthy_bytes = read_sample(
    HEALTHY,
    healthy
)

recovered_bytes = read_sample(
    RECOVERED_MP4,
    recovered
)

print()
print("=" * 110)
print("Healthy vs Recovered")
print("=" * 110)

for i in range(0, 256, 16):

    h = healthy_bytes[i:i+16]
    r = recovered_bytes[i:i+16]

    hhex = " ".join(f"{b:02X}" for b in h)
    rhex = " ".join(f"{b:02X}" for b in r)

    marker = []

    for a, b in zip(h, r):
        marker.append("==" if a == b else "..")

    print(
        f"{i:04X} | "
        f"{hhex:<47} | "
        f"{rhex:<47} | "
        f"{' '.join(marker)}"
    )