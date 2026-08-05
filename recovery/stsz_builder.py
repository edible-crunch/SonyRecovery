from recovery.chunk_parser import parse_chunk
from recovery.access_unit_parser import split_access_units


def build_stsz(filename, chunk_starts):

    """
    Builds a complete STSZ table from verified GOP starts.

    Parameters
    ----------
    filename : str
        Recovered MP4

    chunk_starts : list[int]
        Verified GOP offsets (AUD positions)

    Returns
    -------
    list[int]
        Frame sizes
    """

    stsz = []

    total_video = 0

    for i in range(len(chunk_starts) - 1):

        start = chunk_starts[i]
        end = chunk_starts[i + 1]

        chunk = parse_chunk(
            filename,
            start,
            end
        )

        frames = split_access_units(chunk)

        print(
            f"Chunk {i+1:03d}: "
            f"{len(frames)} frames"
        )

        for frame in frames:

            stsz.append(frame["size"])
            total_video += frame["size"]

    return stsz, total_video