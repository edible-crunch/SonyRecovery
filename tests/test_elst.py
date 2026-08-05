from parsers.atom_reader import read_atoms
from parsers.elst_reader import read_elst


def find_elst(filename):

    atoms = read_atoms(filename)

    for atom in atoms:

        if atom.type == "elst":

            return atom.offset

    raise Exception("elst not found")


def dump(filename):

    print()
    print("=" * 60)
    print(filename)
    print("=" * 60)

    elst = read_elst(
        filename,
        find_elst(filename)
    )

    for i, entry in enumerate(elst.entries):

        print()

        print(f"Entry {i+1}")

        print(
            "Segment Duration:",
            entry["segment_duration"]
        )

        print(
            "Media Time:",
            entry["media_time"]
        )

        print(
            "Media Rate:",
            entry["media_rate"]
        )


dump(
    r"C:\Users\johne\OneDrive\Desktop\ENABLE\C0946.MP4"
)

dump(
    "candidate_clip3.mp4"
)