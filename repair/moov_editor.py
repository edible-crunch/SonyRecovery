import struct


class MoovEditor:

    def __init__(self, filename):

        with open(filename, "rb") as f:
            self.data = bytearray(f.read())

    # -------------------------------------------------

    def find_atom(self, atom_offset):

        size = struct.unpack(">I", self.data[atom_offset:atom_offset+4])[0]

        typ = self.data[
            atom_offset+4:
            atom_offset+8
        ].decode()

        return size, typ

    # -------------------------------------------------

    def replace_atom(self, atom_offset, new_atom):

        old_size, atom_type = self.find_atom(atom_offset)

        print()
        print(f"Replacing {atom_type}")
        print(f"Old size : {old_size:,}")
        print(f"New size : {len(new_atom):,}")

        before = self.data[:atom_offset]
        after = self.data[atom_offset + old_size:]

        self.data = bytearray(
            before +
            new_atom +
            after
        )

        delta = len(new_atom) - old_size

        print(f"Delta : {delta:+,}")

        return delta

    # -------------------------------------------------

    def patch_size(self, atom_offset, delta):

        size = struct.unpack(
            ">I",
            self.data[atom_offset:atom_offset+4]
        )[0]

        size += delta

        self.data[
            atom_offset:
            atom_offset+4
        ] = struct.pack(">I", size)

    # -------------------------------------------------

    def patch_sizes(self, offsets, delta):

        print()
        print("Growing parent atoms")

        for offset in offsets:

            size, typ = self.find_atom(offset)

            self.patch_size(offset, delta)

            print(
                f"{typ:<4} {size:,} -> {size+delta:,}"
            )

    # -------------------------------------------------

    def save(self, filename):

        with open(filename, "wb") as f:

            f.write(self.data)

        print()
        print("[OK] Saved")
        print(filename)