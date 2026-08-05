from atom_reader import read_atoms, read_children


def locate_video_atoms(filename):

    atoms = read_atoms(filename)

    moov = None

    for atom in atoms:

        if atom.type == "moov":
            moov = atom
            break

    if moov is None:
        raise Exception("moov atom not found")

    locations = {}

    def walk(offset, size):

        children = read_children(filename, offset, size, indent=0)

        for child_offset, child_size, child_type in children:

            if child_type in ("stco", "stsc", "stsz", "stsd"):

                locations[child_type] = child_offset

            if child_type in (
                "trak",
                "mdia",
                "minf",
                "stbl",
                "edts",
                "dinf"
            ):

                walk(child_offset, child_size)

    walk(moov.offset, moov.size)

    return locations