from video_tables import get_video_tables
from frame_mapper import build_frame_map
from frame_extractor import extract_frame

print("=== Sony Split Recovery Extractor ===")
print()

mov_file = input("Drag recovered MOV (metadata) here:\n").strip().strip('"')

mp4_file = input("\nDrag recovered MP4 (video payload) here:\n").strip().strip('"')

tables = get_video_tables(mov_file)

frame_map = build_frame_map(
    tables["stco"],
    tables["stsc"],
    tables["stsz"]
)

print()
print("Total Frames :", len(frame_map))

frame_number = int(input("\nFrame number to extract: "))

if frame_number < 1 or frame_number > len(frame_map):
    raise Exception("Invalid frame number")

frame = frame_map[frame_number - 1]

print()
print("Frame Information")
print("-----------------")
print("Frame :", frame["frame"])
print("Chunk :", frame["chunk"])
print("Offset:", frame["offset"])
print("Size  :", frame["size"])

output = f"frame_{frame_number:06d}.bin"

extract_frame(
    mp4_file,
    frame["offset"],
    frame["size"],
    output
)