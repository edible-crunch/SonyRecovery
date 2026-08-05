import shutil
import struct


def write_stco(
    source_moov,
    output_moov,
    stco_atom_offset,
    offsets
):
    """
    Copy a moov atom and overwrite the STCO
    chunk offsets.

    Parameters
    ----------
    source_moov : str
        Original moov.bin

    output_moov : str
        New patched moov.bin

    stco_atom_offset : int
        Byte offset of the STCO atom.

    offsets : list[int]
        New chunk offsets.
    """

    # If we're writing to a different file,
    # make a writable copy first.
    if source_moov != output_moov:
        shutil.copyfile(source_moov, output_moov)

    with open(output_moov, "r+b") as f:

        # Jump to the STCO atom
        f.seek(stco_atom_offset)

        # Read atom header
        atom_size = struct.unpack(">I", f.read(4))[0]
        atom_type = f.read(4).decode()

        if atom_type != "stco":
            raise Exception(
                f"Expected stco atom, found '{atom_type}'."
            )

        # Skip version/flags
        f.read(4)

        # Read entry count
        entry_count = struct.unpack(">I", f.read(4))[0]

        if entry_count != len(offsets):
            raise Exception(
                f"STCO entry mismatch "
                f"({entry_count} != {len(offsets)})"
            )

        print()
        print("Writing STCO")
        print("------------------------------")
        print("Entries :", entry_count)

        # Write offsets
        for offset in offsets:
            f.write(
                struct.pack(">I", offset)
            )

    print()
    print("[OK] STCO patched")
    print(output_moov)