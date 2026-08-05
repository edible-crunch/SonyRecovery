from parsers.video_tables import get_video_tables
from parsers.mdat_reader import locate_mdat

RECOVERED_MOV = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mov\MOV_01m54s_000003.MOV"

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

tables = get_video_tables(RECOVERED_MOV)
mdat = locate_mdat(RECOVERED_MP4)

stco = tables["stco"].offsets

print("=" * 60)
print("OFFSET MATH")
print("=" * 60)

print()

print(f"mdat atom        : {mdat.offset:,}")
print(f"mdat payload     : {mdat.data_offset:,}")

print()

print(f"STCO[0]          : {stco[0]:,}")
print(f"STCO[1]          : {stco[1]:,}")

print()

validated = 1429508

print(f"Validated HEVC   : {validated:,}")

print()

print("Differences")
print("-" * 60)

print(f"Validated - STCO[0]      = {validated - stco[0]:,}")
print(f"Validated - mdat.payload = {validated - mdat.data_offset:,}")
print(f"STCO[0] - payload        = {stco[0] - mdat.data_offset:,}")