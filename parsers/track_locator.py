from parsers.atom_reader import read_atoms


def get_tracks(filename):

    atoms = read_atoms(filename)

    tracks = []

    current = None

    for atom in atoms:

        # -------------------------------------------------
        # Start of a new track
        # -------------------------------------------------

        if atom.type == "trak":

            if current is not None:
                tracks.append(current)

            current = {
                "trak": atom,

                # Parent containers
                "mdia": None,
                "minf": None,
                "stbl": None,

                # Child atoms
                "tkhd": None,
                "mdhd": None,
                "hdlr": None,
                "stsd": None,
                "stco": None,
                "stsc": None,
                "stsz": None,
            }

            continue

        if current is None:
            continue

        # -------------------------------------------------
        # Parent containers
        # -------------------------------------------------

        if atom.type == "mdia":
            current["mdia"] = atom

        elif atom.type == "minf":
            current["minf"] = atom

        elif atom.type == "stbl":
            current["stbl"] = atom

        # -------------------------------------------------
        # Leaf atoms
        # -------------------------------------------------

        elif atom.type == "tkhd":
            current["tkhd"] = atom

        elif atom.type == "mdhd":
            current["mdhd"] = atom

        elif atom.type == "hdlr":
            current["hdlr"] = atom

        elif atom.type == "stsd":
            current["stsd"] = atom

        elif atom.type == "stco":
            current["stco"] = atom

        elif atom.type == "stsc":
            current["stsc"] = atom

        elif atom.type == "stsz":
            current["stsz"] = atom

    if current is not None:
        tracks.append(current)

    return tracks