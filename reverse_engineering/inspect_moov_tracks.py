import struct

MOOV = "moov.bin"


# ---------------------------------------------------------

def be32(buf, off):
    return struct.unpack(">I", buf[off:off+4])[0]


def fourcc(buf, off):
    return buf[off:off+4].decode("ascii", errors="replace")


def find_atoms(buf, start, end, atom_type):

    atoms = []

    p = start

    while p < end:

        size = be32(buf, p)
        typ = fourcc(buf, p + 4)

        if size == 0:
            break

        if typ == atom_type:
            atoms.append((p, size))

        p += size

    return atoms


# ---------------------------------------------------------

with open(MOOV, "rb") as f:
    data = f.read()

print()
print("=" * 80)
print("MOOV TRACK INSPECTOR")
print("=" * 80)

# ---------------------------------------------------------
# Find TRAKs
# ---------------------------------------------------------

traks = find_atoms(
    data,
    8,
    len(data),
    "trak"
)

print()
print("Tracks found :", len(traks))

# ---------------------------------------------------------

for track_num, (trak_off, trak_size) in enumerate(traks, start=1):

    print()
    print("-" * 80)
    print(f"TRACK {track_num}")
    print("-" * 80)

    trak_end = trak_off + trak_size

    # -----------------------------------------------------
    # Find HDLR
    # -----------------------------------------------------

    mdia = find_atoms(
        data,
        trak_off + 8,
        trak_end,
        "mdia"
    )

    handler = "UNKNOWN"

    if mdia:

        mdia_off, mdia_size = mdia[0]

        hdlr = find_atoms(
            data,
            mdia_off + 8,
            mdia_off + mdia_size,
            "hdlr"
        )

        if hdlr:

            hdlr_off, _ = hdlr[0]

            handler = fourcc(
                data,
                hdlr_off + 16
            )

    print("Handler :", handler)

    # -----------------------------------------------------
    # Find STCO
    # -----------------------------------------------------

    stco = find_atoms(
        data,
        trak_off + 8,
        trak_end,
        "stco"
    )

    if not stco:

        print("STCO : NONE")
        continue

    for idx, (off, size) in enumerate(stco, start=1):

        entries = be32(
            data,
            off + 12
        )

        print()
        print(f"STCO {idx}")
        print(f"Offset     : {off:,}")
        print(f"Atom size  : {size:,}")
        print(f"Entries    : {entries:,}")

print()
print("=" * 80)
print("DONE")
print("=" * 80)