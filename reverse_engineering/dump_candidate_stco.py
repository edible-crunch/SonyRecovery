from parsers.video_tables import get_video_tables

tables = get_video_tables("candidate_clip3.mp4")

offsets = tables["stco"].offsets

print("=" * 60)
print("CANDIDATE STCO")
print("=" * 60)

print("Entries:", len(offsets))
print()

for i, off in enumerate(offsets[:20], 1):
    print(f"{i:03d}: {off:,}")