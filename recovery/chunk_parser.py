import os


NAL_NAMES = {
    0: "TRAIL_N",
    1: "TRAIL_R",
    2: "TSA_N",
    3: "TSA_R",
    4: "STSA_N",
    5: "STSA_R",
    6: "RADL_N",
    7: "RADL_R",
    8: "RASL_N",
    9: "RASL_R",

    16: "BLA_W_LP",
    17: "BLA_W_RADL",
    18: "BLA_N_LP",

    19: "IDR_W_RADL",
    20: "IDR_N_LP",
    21: "CRA",

    32: "VPS",
    33: "SPS",
    34: "PPS",
    35: "AUD",
    39: "SEI",
}


def parse_chunk(filename, chunk_start, chunk_end):

    if chunk_end <= chunk_start:
        raise ValueError("Invalid chunk.")

    chunk_size = chunk_end - chunk_start

    with open(filename, "rb") as f:

        f.seek(chunk_start)

        data = f.read(chunk_size)

    nals = []

    pos = 0

    while pos + 4 <= len(data):

        length = int.from_bytes(
            data[pos:pos+4],
            "big"
        )

        if length <= 0:
            break

        if pos + 4 + length > len(data):
            break

        header = data[pos + 4]

        nal_type = (header >> 1) & 0x3F

        nals.append({

            "offset": chunk_start + pos,

            "relative_offset": pos,

            "length": length,

            "type": nal_type,

            "name": NAL_NAMES.get(
                nal_type,
                f"TYPE_{nal_type}"
            )

        })

        pos += 4 + length

    return {

        "chunk_start": chunk_start,

        "chunk_end": chunk_end,

        "chunk_size": chunk_size,

        "bytes_consumed": pos,

        "nals": nals

    }