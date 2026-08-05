from parsers.stco_reader import read_stco

# From test_stco.py we already discovered:
VIDEO_STCO_OFFSET = 83355


def dump(filename):

    print()
    print("=" * 60)
    print(filename)
    print("=" * 60)

    stco = read_stco(
        filename,
        VIDEO_STCO_OFFSET
    )

    print("Entries:", len(stco.offsets))

    print()

    for i, offset in enumerate(stco.offsets[:10], start=1):

        print(f"{i:3}: {offset:,}")


dump("moov.bin")

dump("patched_moov.bin")