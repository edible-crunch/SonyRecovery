import struct


class Mdat:

    def __init__(self):

        self.offset = 0
        self.size = 0
        self.data_offset = 0


def locate_mdat(filename):

    with open(filename, "rb") as f:

        while True:

            pos = f.tell()

            header = f.read(8)

            if len(header) < 8:
                break

            size, typ = struct.unpack(">I4s", header)

            typ = typ.decode(errors="ignore")

            header_size = 8

            if size == 1:

                size = struct.unpack(">Q", f.read(8))[0]

                header_size = 16

            if typ == "mdat":

                m = Mdat()

                m.offset = pos
                m.size = size
                m.data_offset = pos + header_size

                return m

            if size == 0:
                break

            f.seek(pos + size)

    raise Exception("mdat not found")