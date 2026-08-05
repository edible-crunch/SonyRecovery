import shutil

from parsers.atom_reader import read_atoms, find_atom
from parsers.mdat_reader import locate_mdat


def copy_range(src, dst, offset, size):

    src.seek(offset)

    remaining = size

    while remaining:

        chunk = src.read(min(1024 * 1024, remaining))

        if not chunk:
            break

        dst.write(chunk)

        remaining -= len(chunk)


def build_mp4(

    healthy_mp4,
    patched_moov,
    recovered_mp4,
    output_mp4

):

    print()
    print("=" * 60)
    print("MP4 BUILDER")
    print("=" * 60)

    atoms = read_atoms(healthy_mp4)

    ftyp = find_atom(atoms, "ftyp")

    if ftyp is None:
        raise Exception("FTYP not found.")

    mdat = locate_mdat(recovered_mp4)

    print()
    print("FTYP")
    print(
        f"Offset={ftyp.offset:,} Size={ftyp.size:,}"
    )

    print()

    print("MDAT")
    print(
        f"Offset={mdat.offset:,} Size={mdat.size:,}"
    )

    with open(healthy_mp4, "rb") as healthy, \
         open(patched_moov, "rb") as moov, \
         open(recovered_mp4, "rb") as recovered, \
         open(output_mp4, "wb") as out:

        #
        # FTYP
        #

        copy_range(
            healthy,
            out,
            ftyp.offset,
            ftyp.size
        )

        #
        # MOOV
        #

        shutil.copyfileobj(
            moov,
            out
        )

        #
        # MDAT
        #

        copy_range(
            recovered,
            out,
            mdat.offset,
            mdat.size
        )

    print()

    print("[OK] MP4 built")

    print(output_mp4)