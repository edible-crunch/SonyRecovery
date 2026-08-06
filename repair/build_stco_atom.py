import struct


def build_stco_atom(offsets):
    """
    Build a complete STCO atom.

    Parameters
    ----------
    offsets : iterable[int]
        Absolute chunk offsets.

    Returns
    -------
    bytes
        Complete STCO atom.
    """

    payload = bytearray()

    # version + flags
    payload += b"\x00\x00\x00\x00"

    # entry count
    payload += struct.pack(">I", len(offsets))

    # chunk offsets
    for offset in offsets:
        payload += struct.pack(">I", offset)

    atom = bytearray()

    atom += struct.pack(">I", len(payload) + 8)
    atom += b"stco"
    atom += payload

    return bytes(atom)


if __name__ == "__main__":

    # Simple self-test
    test_offsets = [
        100,
        200,
        300,
    ]

    atom = build_stco_atom(test_offsets)

    print("=" * 60)
    print("STCO BUILDER")
    print("=" * 60)
    print()
    print("Entries :", len(test_offsets))
    print("Atom size :", len(atom))

    with open("test_stco.bin", "wb") as f:
        f.write(atom)

    print()
    print("[OK] test_stco.bin written")
