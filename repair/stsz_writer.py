import shutil
import struct


def write_stsz(
    source_moov,
    output_moov,
    stsz_atom_offset,
    rebuilt_stsz
):
    """
    Replace the STSZ atom with a rebuilt one.

    source_moov
        Original moov.bin

    output_moov
        New patched moov.bin

    stsz_atom_offset
        Offset of the STSZ atom inside moov.bin

    rebuilt_stsz
        Binary STSZ atom.
    """

    shutil.copyfile(source_moov, output_moov)

    with open(output_moov, "r+b") as f:

        f.seek(stsz_atom_offset)

        old_size = struct.unpack(">I", f.read(4))[0]

        f.seek(stsz_atom_offset)

        old_atom = f.read(old_size)

        if old_atom[4:8] != b"stsz":
            raise Exception("Not an STSZ atom.")

    old_size = len(old_atom)
    new_size = len(rebuilt_stsz)

    with open(output_moov, "rb") as f:
        before = f.read(stsz_atom_offset)
        f.seek(stsz_atom_offset + old_size)
        after = f.read()

    with open(output_moov, "wb") as f:

        f.write(before)
        f.write(rebuilt_stsz)
        f.write(after)

    delta = new_size - old_size

    print()
    print("=" * 60)
    print("STSZ PATCH")
    print("=" * 60)

    print(f"Old size : {old_size:,}")
    print(f"New size : {new_size:,}")
    print(f"Delta    : {delta:+,}")

    return delta