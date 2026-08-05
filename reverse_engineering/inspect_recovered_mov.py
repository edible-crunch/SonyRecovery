from parsers.atom_reader import read_atoms

FILE = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mov\MOV_01m54s_000003.MOV"

atoms = read_atoms(FILE)

print("=" * 80)
print("ALL ATOMS")
print("=" * 80)

for atom in atoms:
    indent = "    " * atom.level
    print(f"{indent}{atom.type:6}  offset={atom.offset:,}  size={atom.size:,}")