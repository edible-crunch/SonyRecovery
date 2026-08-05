from video_tables import get_video_tables
from frame_mapper import build_frame_map

file = input("Drag MP4/MOV here:\n").strip().strip('"')

tables = get_video_tables(file)

frame_map = build_frame_map(
    tables["stco"],
    tables["stsc"],
    tables["stsz"]
)

print()
print("FRAME 58-62")
print("-" * 60)
print(f"{'Frame':>6} {'Chunk':>6} {'Offset':>12} {'Size':>10}")

for item in frame_map[57:62]:

    print(
        f"{item['frame']:6}"
        f"{item['chunk']:6}"
        f"{item['offset']:12}"
        f"{item['size']:10}"
    )