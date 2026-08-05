# ============================================
# HEVC Utility Library
# ============================================

NAL_TYPES = {
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
    36: "EOS",
    37: "EOB",
    38: "FD",
    39: "PREFIX_SEI",
    40: "SUFFIX_SEI"
}


def parse_header(data):

    if len(data) < 2:
        return None

    b0 = data[0]
    b1 = data[1]

    forbidden_zero = (b0 >> 7) & 1

    nal_type = (b0 >> 1) & 0x3F

    layer_id = ((b0 & 1) << 5) | (b1 >> 3)

    temporal_id = b1 & 0x07

    return {
        "forbidden_zero": forbidden_zero,
        "nal_type": nal_type,
        "nal_name": NAL_TYPES.get(nal_type, "UNKNOWN"),
        "layer_id": layer_id,
        "temporal_id": temporal_id
    }


def looks_like_hevc_header(data):

    info = parse_header(data)

    if info is None:
        return False

    if info["forbidden_zero"] != 0:
        return False

    if info["layer_id"] != 0:
        return False

    if info["temporal_id"] == 0:
        return False

    return True