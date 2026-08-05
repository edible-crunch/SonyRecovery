import struct

MOOV = "moov.bin"


# ============================================================
# Known ISO BMFF / QuickTime container atoms
# ============================================================

CONTAINERS = {
    "moov",
    "trak",
    "mdia",
    "minf",
    "stbl",
    "edts",
    "dinf",
    "udta",
    "meta",
    "ilst",
}


# ============================================================
# Helpers
# ============================================================

def be32(data, offset):
    return struct.unpack_from(">I", data, offset)[0]


def be64(data, offset):
    return struct.unpack_from(">Q", data, offset)[0]


def fourcc(data, offset):
    return data[offset:offset + 4].decode(
        "ascii",
        errors="replace"
    )


# ============================================================
# Recursive walker
# ============================================================

def walk_atoms(data, start, end, depth=0):

    pos = start

    while pos + 8 <= end:

        size = be32(data, pos)
        atom_type = fourcc(data, pos + 4)

        header_size = 8

        # ----------------------------------------------------
        # Extended 64-bit atom size
        # ----------------------------------------------------

        if size == 1:

            if pos + 16 > end:
                break

            size = be64(data, pos + 8)
            header_size = 16

        # ----------------------------------------------------
        # Size 0 means extends to end of parent
        # ----------------------------------------------------

        elif size == 0:

            size = end - pos

        # ----------------------------------------------------
        # Sanity checks
        # ----------------------------------------------------

        if size < header_size:
            print(
                "  " * depth
                + f"[INVALID] offset={pos:,} size={size}"
            )
            break

        atom_end = pos + size

        if atom_end > end:

            print(
                "  " * depth
                + f"[OUT OF RANGE] "
                  f"{atom_type} "
                  f"offset={pos:,} "
                  f"size={size:,}"
            )

            break

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        indent = "  " * depth

        extra = ""

        if atom_type == "stco" and size >= 16:

            entry_count = be32(
                data,
                pos + 12
            )

            extra = (
                f"  <<< STCO "
                f"entries={entry_count:,}"
            )

        elif atom_type == "co64" and size >= 16:

            entry_count = be32(
                data,
                pos + 12
            )

            extra = (
                f"  <<< CO64 "
                f"entries={entry_count:,}"
            )

        elif atom_type == "stsz" and size >= 20:

            sample_size = be32(
                data,
                pos + 12
            )

            sample_count = be32(
                data,
                pos + 16
            )

            extra = (
                f"  <<< STSZ "
                f"samples={sample_count:,} "
                f"default={sample_size:,}"
            )

        elif atom_type == "stsc" and size >= 16:

            entry_count = be32(
                data,
                pos + 12
            )

            extra = (
                f"  <<< STSC "
                f"entries={entry_count:,}"
            )

        print(
            f"{indent}"
            f"{atom_type}  "
            f"offset={pos:,}  "
            f"size={size:,}"
            f"{extra}"
        )

        # ----------------------------------------------------
        # Recurse into known containers
        # ----------------------------------------------------

        if atom_type in CONTAINERS:

            child_start = pos + header_size

            # FullBox 'meta' has version/flags before children.
            if atom_type == "meta":
                child_start += 4

            if child_start < atom_end:

                walk_atoms(
                    data,
                    child_start,
                    atom_end,
                    depth + 1
                )

        pos = atom_end


# ============================================================
# Main
# ============================================================

with open(MOOV, "rb") as f:
    data = f.read()


print()
print("=" * 100)
print("MOOV ATOM TREE")
print("=" * 100)
print()

print(f"File       : {MOOV}")
print(f"File size  : {len(data):,}")
print()

# moov.bin should itself begin with a moov atom.
if len(data) < 8:

    raise Exception(
        "moov.bin is too small to contain a valid atom."
    )


root_size = be32(data, 0)
root_type = fourcc(data, 4)

print(f"Root type  : {root_type}")
print(f"Root size  : {root_size:,}")
print()

if root_type != "moov":

    print(
        "[WARNING] File does not begin with a moov atom."
    )

print("-" * 100)

walk_atoms(
    data,
    0,
    len(data)
)

print("-" * 100)
print()
print("=" * 100)
print("DONE")
print("=" * 100)