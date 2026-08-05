import struct

CONTAINERS = {
    "moov",
    "trak",
    "mdia",
    "minf",
    "stbl",
    "edts",
    "dinf",
    "udta",
    "meta",
    "ilst"
}


class Atom:

    def __init__(self, offset, size, typ, level=0):
        self.offset = offset
        self.size = size
        self.type = typ
        self.level = level

    def __repr__(self):
        return f"{'    '*self.level}{self.type} @ {self.offset} ({self.size})"


def read_atoms(filename):

    atoms = []

    with open(filename, "rb") as f:

        f.seek(0, 2)
        filesize = f.tell()
        f.seek(0)

        walk_atoms(f, 0, filesize, atoms, 0)

    return atoms


def walk_atoms(f, start, end, atoms, level):

    pos = start

    while pos + 8 <= end:

        f.seek(pos)

        header = f.read(8)

        if len(header) < 8:
            return

        size, typ = struct.unpack(">I4s", header)

        typ = typ.decode(errors="ignore")

        header_size = 8

        if size == 1:

            size = struct.unpack(">Q", f.read(8))[0]
            header_size = 16

        if size == 0:
            return

        atom = Atom(pos, size, typ, level)
        atoms.append(atom)

        if typ in CONTAINERS:

            walk_atoms(
                f,
                pos + header_size,
                pos + size,
                atoms,
                level + 1
            )

        pos += size


def print_atoms(atoms):

    for atom in atoms:
        print(atom)


def find_atom(atoms, atom_type):

    for atom in atoms:

        if atom.type == atom_type:
            return atom

    return None