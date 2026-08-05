from parsers.atom_reader import read_atoms
from parsers.stco_reader import read_stco

atoms = read_atoms("candidate_clip3.mp4")

stcos = [a for a in atoms if a.type == "stco"]

print(f"Found {len(stcos)} STCO atoms\n")

for i, atom in enumerate(stcos, 1):
    stco = read_stco("candidate_clip3.mp4", atom.offset, i)

    print(f"Track {i}")
    print(f"Offset : {atom.offset}")
    print(f"Entries: {len(stco.offsets)}")
    print("First five:")

    for x in stco.offsets[:5]:
        print(f"  {x:,}")

    print()