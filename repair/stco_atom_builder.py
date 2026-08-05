import struct


def build_stco_atom(offsets):
    """
    Build a complete STCO atom.

    Parameters
    ----------
    offsets : list[int]

    Returns
    -------
    bytes
        Complete STCO atom.
    """

    payload = bytearray()

    # ----------------------------------------------------
    # version + flags
    # ----------------------------------------------------

    payload += b"\x00\x00\x00\x00"

    # ----------------------------------------------------
    # entry count
    # ----------------------------------------------------

    payload += struct.pack(
        ">I",
        len(offsets)
    )

    # ----------------------------------------------------
    # chunk offsets
    # ----------------------------------------------------

    for offset in offsets:

        payload += struct.pack(
            ">I",
            offset
        )

    # ----------------------------------------------------
    # atom
    # ----------------------------------------------------

    atom = bytearray()

    atom += struct.pack(
        ">I",
        len(payload) + 8
    )

    atom += b"stco"

    atom += payload

    return bytes(atom)


# ----------------------------------------------------------
# Optional helper
# ----------------------------------------------------------

def write_stco_atom(
    filename,
    offsets,
):
    """
    Convenience wrapper.
    """

    atom = build_stco_atom(
        offsets
    )

    with open(filename, "wb") as f:

        f.write(atom)

    return atom