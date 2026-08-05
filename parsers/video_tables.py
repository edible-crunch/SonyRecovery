from parsers.video_track import get_video_atoms

from parsers.stco_reader import read_stco
from parsers.stsc_reader import read_stsc
from parsers.stsz_reader import read_stsz


def get_video_tables(filename):

    video = get_video_atoms(filename)

    stco = read_stco(
        filename,
        video["stco"].offset
    )

    stsc = read_stsc(
        filename,
        video["stsc"].offset
    )

    stsz = read_stsz(
        filename,
        video["stsz"].offset
    )

    return {
        # Parsed tables
        "stco": stco,
        "stsc": stsc,
        "stsz": stsz,

        # Atom locations inside the MOV
        "stco_atom_offset": video["stco"].offset,
        "stsc_atom_offset": video["stsc"].offset,
        "stsz_atom_offset": video["stsz"].offset,
    }