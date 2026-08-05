from validation.ffprobe import FFProbe

probe = FFProbe("ffmpeg/ffprobe.exe")

mp4 = input("Recovered MP4:\n").strip('"')

data = probe.packets(mp4)

packets = data["packets"]

print()

print("=" * 60)
print("VIDEO PACKETS")
print("=" * 60)

print()

print("Count:", len(packets))

print()

for packet in packets[:10]:

    print(
        packet["pos"],
        packet["size"],
        packet.get("pts_time")
    )