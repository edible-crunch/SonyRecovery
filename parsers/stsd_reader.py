import struct


def read_stsd(filename, stsd_offset):

    with open(filename, "rb") as f:

        f.seek(stsd_offset)

        atom_size = struct.unpack(">I", f.read(4))[0]
        atom_type = f.read(4).decode()

        if atom_type != "stsd":
            raise Exception("Not an stsd atom!")

        # Version + Flags
        f.read(4)

        # Number of sample descriptions
        entry_count = struct.unpack(">I", f.read(4))[0]

        print()
        print("Atom Size :", atom_size)
        print("Atom Type :", atom_type)
        print("Entries   :", entry_count)

        # Sample Entry
        sample_entry_offset = f.tell()

        sample_entry_size = struct.unpack(">I", f.read(4))[0]
        sample_entry_type = f.read(4).decode()

        print()
        print("Sample Entry")
        print("----------------")
        print("Offset :", sample_entry_offset)
        print("Size   :", sample_entry_size)
        print("Type   :", sample_entry_type)

        return sample_entry_offset, sample_entry_size