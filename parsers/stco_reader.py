import struct


class STCO:

    def __init__(self):
        self.track_number = 0
        self.offsets = []


def read_stco(filename, atom_offset, track_number=0):

    stco = STCO()
    stco.track_number = track_number

    with open(filename, "rb") as f:

        f.seek(atom_offset)

        atom_size = struct.unpack(">I", f.read(4))[0]
        atom_type = f.read(4).decode()

        if atom_type != "stco":
            raise Exception("Not an stco atom!")

        # version + flags
        f.read(4)

        entry_count = struct.unpack(">I", f.read(4))[0]

        for _ in range(entry_count):
            stco.offsets.append(
                struct.unpack(">I", f.read(4))[0]
            )

    return stco