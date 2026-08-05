from parsers.video_tables import get_video_tables

tables = get_video_tables("candidate_clip3.mp4")

offset = tables["stco"].offsets[0]

print("First STCO:", offset)

with open("candidate_clip3.mp4", "rb") as f:
    f.seek(offset)
    data = f.read(64)

for i in range(0, len(data), 16):
    chunk = data[i:i+16]
    print(
        f"{offset+i:08X}:",
        " ".join(f"{b:02X}" for b in chunk)
    )