from parsers.atom_reader import read_atoms

atoms = read_atoms("moov.bin")

print("=" * 70)
print("ATOM TREE")
print("=" * 70)

for atom in atoms:
    indent = "    " * atom.level
    print(
        f"{indent}{atom.type:<4} "
        f"offset={atom.offset:,} "
        f"size={atom.size:,}"
    )

print()
print("=" * 70)
print("PARENT CHAIN")
print("=" * 70)

wanted = ["moov", "trak", "mdia", "minf", "stbl", "stsz", "stco"]

for atom in atoms:
    if atom.type in wanted:
        print(
            f"{atom.type:<4} "
            f"offset={atom.offset:,} "
            f"size={atom.size:,}"
        )