from locators.stco_locator import find_stco_atoms
from parsers.stco_reader import read_stco

moov = "moov.bin"

atoms = find_stco_atoms(moov)

print()
print("STCO atoms found:", len(atoms))
print()

for i, atom in enumerate(atoms, 1):

    stco = read_stco(
        moov,
        atom,
        i
    )

    print(f"Track {i}")
    print("Offset:", atom)
    print("Entries:", len(stco.offsets))

    print("First five offsets:")

    for value in stco.offsets[:5]:
        print(" ", value)

    print()