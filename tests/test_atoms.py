from atom_reader import read_atoms, print_atoms, find_atom

file = input("Drag MP4/MOV here:\n").strip().strip('"')

atoms = read_atoms(file)

print()
print("ATOM TREE")
print("-" * 40)

print_atoms(atoms)

print()

for name in ["stsd", "stco", "stsc", "stsz"]:

    atom = find_atom(atoms, name)

    if atom:
        print(name, "found at", atom.offset)
    else:
        print(name, "NOT FOUND")