from parsers.atom_reader import read_atoms, find_atom


def get_video_atoms(filename):

    atoms = read_atoms(filename)

    stsd = find_atom(atoms, "stsd")
    stco = find_atom(atoms, "stco")
    stsc = find_atom(atoms, "stsc")
    stsz = find_atom(atoms, "stsz")

    if not all([stsd, stco, stsc, stsz]):
        raise Exception("Video sample table is incomplete.")

    return {
        "stsd": stsd,
        "stco": stco,
        "stsc": stsc,
        "stsz": stsz,
    }