import struct


def walk_sample_entry(filename, sample_entry_offset, sample_entry_size):

    with open(filename, "rb") as f:

        #
        # Skip:
        # 8 bytes  sample entry header (size + type)
        # 78 bytes hvc1 fixed fields
        #
        # Child boxes begin after that.
        #
        pos = sample_entry_offset + 86
        end = sample_entry_offset + sample_entry_size

        print()
        print("Child Boxes")
        print("-----------------------")

        while pos + 8 <= end:

            f.seek(pos)

            header = f.read(8)

            if len(header) < 8:
                break

            size, typ = struct.unpack(">I4s", header)

            typ = typ.decode(errors="ignore")

            print(f"{typ} @ {pos} ({size})")

            if size < 8:
                break

            pos += size