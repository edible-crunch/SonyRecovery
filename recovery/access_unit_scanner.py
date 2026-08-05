from parsers.mdat_reader import locate_mdat
from repair.hevc import parse_header


class Candidate:

    def __init__(self, offset, nal_length, header):

        self.offset = offset
        self.nal_length = nal_length
        self.header = header


def scan_candidates(
    mp4_path,
    step=16,
    max_candidates=100
):

    mdat = locate_mdat(mp4_path)

    start = mdat.data_offset
    end = mdat.data_offset + mdat.size

    candidates = []

    with open(mp4_path, "rb") as f:

        pos = start

        while pos + 6 < end:

            f.seek(pos)

            header_bytes = f.read(6)

            if len(header_bytes) < 6:
                break

            nal_length = int.from_bytes(
                header_bytes[0:4],
                "big"
            )

            if nal_length <= 0:
                pos += step
                continue

            remaining = end - pos - 4

            if nal_length > remaining:
                pos += step
                continue

            header = parse_header(header_bytes[4:6])

            if header is None:
                pos += step
                continue

            if header["forbidden_zero"] != 0:
                pos += step
                continue

            if header["layer_id"] != 0:
                pos += step
                continue

            if header["temporal_id"] <= 0:
                pos += step
                continue

            candidates.append(
                Candidate(
                    pos,
                    nal_length,
                    header
                )
            )

            if len(candidates) >= max_candidates:
                break

            pos += step

    return candidates