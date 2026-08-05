import struct


class EditList:

    def __init__(self):

        self.entries = []


def read_elst(filename, atom_offset):

    elst = EditList()

    with open(filename, "rb") as f:

        f.seek(atom_offset)

        size = struct.unpack(">I", f.read(4))[0]
        typ = f.read(4).decode()

        if typ != "elst":
            raise Exception("Not an elst atom")

        version = f.read(1)[0]

        # flags
        f.read(3)

        entry_count = struct.unpack(">I", f.read(4))[0]

        for _ in range(entry_count):

            if version == 1:

                segment_duration = struct.unpack(">Q", f.read(8))[0]
                media_time = struct.unpack(">q", f.read(8))[0]

            else:

                segment_duration = struct.unpack(">I", f.read(4))[0]
                media_time = struct.unpack(">i", f.read(4))[0]

            media_rate = struct.unpack(">h", f.read(2))[0]

            f.read(2)

            elst.entries.append({
                "segment_duration": segment_duration,
                "media_time": media_time,
                "media_rate": media_rate
            })

    return elst