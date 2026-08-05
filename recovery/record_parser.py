import struct

from repair.hevc import parse_header


class Record:

    def __init__(self):

        self.offset = 0

        self.length = 0

        self.tag = 0

        self.header = None

        self.payload = b""


def parse_record(data, offset):

    if offset + 8 > len(data):

        return None

    length = struct.unpack("<I", data[offset:offset + 4])[0]

    tag = struct.unpack("<I", data[offset + 4:offset + 8])[0]

    if length == 0:

        return None

    if length > 1000000:

        return None

    end = offset + 8 + length

    if end > len(data):

        return None

    payload = data[offset + 8:end]

    if len(payload) < 2:

        return None

    header = parse_header(payload[:2])

    if header is None:

        return None

    if header["forbidden_zero"] != 0:

        return None

    r = Record()

    r.offset = offset

    r.length = length

    r.tag = tag

    r.header = header

    r.payload = payload

    return r