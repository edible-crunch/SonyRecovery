from parsers.video_tables import get_video_tables

RECOVERED_MOV = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mov\MOV_01m54s_000003.MOV"
)

VIDEO_SAMPLES_PER_CHUNK = 60

tables = get_video_tables(RECOVERED_MOV)

stco = tables["stco"]
stsz = tables["stsz"]
stsc = tables["stsc"]

print()
print("=" * 80)
print("RECOVERED VIDEO TRACK")
print("=" * 80)

print()

print(f"STCO entries          : {len(stco.offsets)}")
print(f"STSZ samples          : {len(stsz)}")

print()

print("STSC")

for entry in stsc:
    print(entry)

print()

expected_chunks = 0

for first_chunk, samples_per_chunk, _ in stsc:

    # We only have one STSC entry for Clip 3
    expected_chunks = (
        len(stsz) + samples_per_chunk - 1
    ) // samples_per_chunk

print(f"Expected chunks from STSZ : {expected_chunks}")

print()

if expected_chunks == len(stco.offsets):

    print("[OK] STCO matches STSZ.")

else:

    print("[WARNING] STCO does NOT match STSZ.")
    print(
        f"Difference : {expected_chunks - len(stco.offsets):+d}"
    )