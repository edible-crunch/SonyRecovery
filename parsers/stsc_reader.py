import struct


def read_stsc(filename, stsc_offset):

    with open(filename, "rb") as f:

        f.seek(stsc_offset)

        atom_size = struct.unpack(">I", f.read(4))[0]
        atom_type = f.read(4).decode()

        if atom_type != "stsc":
            raise Exception("Not an stsc atom!")

        # Version + Flags
        f.read(4)

        # Number of entries
        entry_count = struct.unpack(">I", f.read(4))[0]

        print()
        print("Atom Size :", atom_size)
        print("Atom Type :", atom_type)
        print("Entries   :", entry_count)
        print()

        entries = []

        for _ in range(entry_count):

            first_chunk = struct.unpack(">I", f.read(4))[0]
            samples_per_chunk = struct.unpack(">I", f.read(4))[0]
            sample_description = struct.unpack(">I", f.read(4))[0]

            entries.append(
                (
                    first_chunk,
                    samples_per_chunk,
                    sample_description
                )
            )

        return entries