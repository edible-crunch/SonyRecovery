import struct

from parsers.track_locator import get_tracks


REFERENCE = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)


def handler_type(filename, hdlr_atom):

    with open(filename, "rb") as f:

        #
        # hdlr atom
        #
        # size
        # type
        # version/flags
        # pre_defined
        # handler_type
        #

        f.seek(hdlr_atom.offset + 16)

        return f.read(4).decode(errors="ignore")


tracks = get_tracks(REFERENCE)

print()
print("=" * 70)
print("TRACK LOCATOR")
print("=" * 70)

for i, track in enumerate(tracks, 1):

    print()

    print(f"Track {i}")

    print("-" * 40)

    typ = handler_type(
        REFERENCE,
        track["hdlr"]
    )

    print("Handler :", typ)

    for atom_name in (
        "stsd",
        "stco",
        "stsc",
        "stsz",
    ):

        atom = track[atom_name]

        if atom is None:
            continue

        print(
            f"{atom_name:<5} "
            f"offset={atom.offset:,} "
            f"size={atom.size:,}"
        )