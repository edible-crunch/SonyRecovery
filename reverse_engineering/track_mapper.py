from locators.stco_locator import find_stco_atoms
from parsers.stco_reader import read_stco


MOOV = "moov.bin"


def main():

    atoms = find_stco_atoms(MOOV)

    all_chunks = []

    for track_number, atom in enumerate(atoms, start=1):

        stco = read_stco(MOOV, atom, track_number)

        for chunk_number, offset in enumerate(stco.offsets, start=1):

            all_chunks.append({
                "track": track_number,
                "chunk": chunk_number,
                "offset": offset
            })

    all_chunks.sort(key=lambda x: x["offset"])

    print()
    print("=" * 72)
    print("INTERLEAVED CHUNK MAP")
    print("=" * 72)
    print()

    for c in all_chunks[:60]:
        print(
            f"{c['offset']:>10,}   "
            f"Track {c['track']}   "
            f"Chunk {c['chunk']}"
        )


if __name__ == "__main__":
    main()