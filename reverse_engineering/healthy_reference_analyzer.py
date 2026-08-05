from parsers.video_tables import get_video_tables
from recovery.frame_mapper import build_frame_map

HEALTHY = r"C:\Users\johne\OneDrive\Desktop\ENABLE\C0946.MP4"

tables = get_video_tables(HEALTHY)

frame_map = build_frame_map(
    tables["stco"].offsets,
    tables["stsc"],
    tables["stsz"]
)

frames_to_check = [
    1,
    2,
    3,
    10,
    30,
    60,
    61,
    120,
    240,
    480,
    960
]

NAL_NAMES = {
    32: "VPS",
    33: "SPS",
    34: "PPS",
    35: "AUD",
    39: "SEI",
    19: "IDR_W_RADL",
    20: "IDR_N_LP",
    21: "CRA",
}

with open(HEALTHY, "rb") as f:

    for frame_number in frames_to_check:

        if frame_number > len(frame_map):
            continue

        frame = frame_map[frame_number - 1]

        f.seek(frame["offset"])

        sample = f.read(frame["size"])

        print()
        print("=" * 70)
        print(f"FRAME {frame_number}")
        print("=" * 70)
        print(f"Offset : {frame['offset']:,}")
        print(f"Size   : {frame['size']:,}")

        pos = 0

        for nal in range(1, 8):

            if pos + 4 > len(sample):
                break

            length = int.from_bytes(
                sample[pos:pos+4],
                "big"
            )

            if length <= 0:
                break

            if pos + 4 + length > len(sample):
                break

            header = sample[pos+4]

            nal_type = (header >> 1) & 0x3F

            print(
                f"NAL {nal:<2} "
                f"Type {nal_type:<2} "
                f"{NAL_NAMES.get(nal_type,'?'):<12} "
                f"Length {length:,}"
            )

            pos += 4 + length