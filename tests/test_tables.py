from video_tables import get_video_tables

file = input("Drag MP4/MOV here:\n").strip().strip('"')

tables = get_video_tables(file)

print()
print("SUMMARY")
print("------------------------")

print("Chunks :", len(tables["stco"]))
print("Samples:", len(tables["stsz"]))
print("Mappings:", len(tables["stsc"]))