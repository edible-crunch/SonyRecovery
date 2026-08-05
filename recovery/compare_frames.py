from video_tables import get_video_tables
from frame_mapper import build_frame_map


def read_sample(file, frame_number):

    tables = get_video_tables(file)

    frame_map = build_frame_map(
        tables["stco"],
        tables["stsc"],
        tables["stsz"]
    )

    frame = frame_map[frame_number - 1]

    with open(file, "rb") as f:
        f.seek(frame["offset"])
        data = f.read(min(frame["size"], 128))

    return frame, data


def hexdump(data):

    for i in range(0, len(data), 16):

        chunk = data[i:i+16]

        hexs = " ".join(f"{b:02X}" for b in chunk)
        text = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)

        print(f"{i:04X}  {hexs:<47} {text}")


healthy = input("Healthy MP4:\n").strip().strip('"')
mov = input("Recovered MOV:\n").strip().strip('"')
recovered = input("Recovered MP4:\n").strip().strip('"')

frame_number = int(input("Frame number: "))

healthy_frame, healthy_data = read_sample(
    healthy,
    frame_number
)

tables = get_video_tables(mov)

frame_map = build_frame_map(
    tables["stco"],
    tables["stsc"],
    tables["stsz"]
)

frame = frame_map[frame_number - 1]

with open(recovered, "rb") as f:

    f.seek(frame["offset"])
    recovered_data = f.read(min(frame["size"], 128))

print()
print("=" * 70)
print("HEALTHY")
print("=" * 70)

print(healthy_frame)

hexdump(healthy_data)

print()

print("=" * 70)
print("RECOVERED")
print("=" * 70)

print(frame)

hexdump(recovered_data)