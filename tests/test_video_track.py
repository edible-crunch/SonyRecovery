from video_track import get_video_atoms

file = input("Drag MP4/MOV here:\n").strip().strip('"')

atoms = get_video_atoms(file)

print()

for name in atoms:

    atom = atoms[name]

    print(f"{name} -> {atom.offset}")