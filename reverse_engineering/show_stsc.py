from parsers.video_track import get_video_atoms
from parsers.stsc_reader import read_stsc

mov = input("Recovered MOV:\n").strip('"')

video = get_video_atoms(mov)

entries = read_stsc(
    mov,
    video["stsc"].offset
)

print()
print("=" * 60)
print("STSC ENTRIES")
print("=" * 60)

for i, entry in enumerate(entries, 1):

    first_chunk, samples_per_chunk, sample_description = entry

    print(
        f"{i}: "
        f"first_chunk={first_chunk}, "
        f"samples_per_chunk={samples_per_chunk}, "
        f"sample_description={sample_description}"
    )