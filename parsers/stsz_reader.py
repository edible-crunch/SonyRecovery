import struct


def read_stsz(filename, stsz_offset):

    with open(filename, "rb") as f:

        f.seek(stsz_offset)

        atom_size = struct.unpack(">I", f.read(4))[0]
        atom_type = f.read(4).decode()

        if atom_type != "stsz":
            raise Exception("Not an stsz atom!")

        # Version + Flags
        f.read(4)

        # Default sample size
        sample_size = struct.unpack(">I", f.read(4))[0]

        # Number of samples
        sample_count = struct.unpack(">I", f.read(4))[0]

        print()
        print("Atom Size   :", atom_size)
        print("Atom Type   :", atom_type)
        print("Sample Size :", sample_size)
        print("Samples     :", sample_count)
        print()

        sizes = []

        if sample_size == 0:

            for _ in range(sample_count):

                sizes.append(
                    struct.unpack(">I", f.read(4))[0]
                )

        else:

            sizes = [sample_size] * sample_count

        return sizes