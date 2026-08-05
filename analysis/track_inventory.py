from parsers.atom_reader import read_atoms


def inventory(filename):

    atoms = read_atoms(filename)

    print()
    print("=" * 60)
    print("TRACK INVENTORY")
    print("=" * 60)

    print()

    tracks = [
        a for a in atoms
        if a.type == "trak"
    ]

    print(f"Tracks Found : {len(tracks)}")
    print()

    for i, track in enumerate(tracks, 1):

        print("-" * 60)
        print(f"Track {i}")
        print("-" * 60)

        print(
            f"Offset : {track.offset:,}"
        )

        print(
            f"Size   : {track.size:,}"
        )

        print()