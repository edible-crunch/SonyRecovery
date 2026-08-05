import struct


class HVCC:

    def __init__(self):

        self.configuration_version = 0

        self.profile_space = 0
        self.tier_flag = 0
        self.profile_idc = 0

        self.compatibility_flags = 0
        self.constraint_flags = 0

        self.level_idc = 0

        self.nalu_length_size = 0

        self.arrays = []


def parse_hvcc(filename):

    with open(filename, "rb") as f:

        data = f.read()

    hvcc = HVCC()

    # Skip MP4 box header (size + type)
    p = 8

    hvcc.configuration_version = data[p]
    p += 1

    byte = data[p]
    p += 1

    hvcc.profile_space = byte >> 6
    hvcc.tier_flag = (byte >> 5) & 1
    hvcc.profile_idc = byte & 0x1F

    hvcc.compatibility_flags = struct.unpack(">I", data[p:p+4])[0]
    p += 4

    hvcc.constraint_flags = int.from_bytes(data[p:p+6], "big")
    p += 6

    hvcc.level_idc = data[p]
    p += 1

    # reserved(4) + min_spatial_segmentation_idc(12)
    p += 2

    # reserved(6) + parallelismType(2)
    p += 1

    # reserved(6) + chromaFormat(2)
    p += 1

    # reserved(5) + bitDepthLumaMinus8(3)
    p += 1

    # reserved(5) + bitDepthChromaMinus8(3)
    p += 1

    # avgFrameRate
    p += 2

    # constantFrameRate(2)
    # numTemporalLayers(3)
    # temporalIdNested(1)
    # lengthSizeMinusOne(2)
    byte = data[p]
    p += 1

    hvcc.nalu_length_size = (byte & 0x03) + 1

    num_arrays = data[p]
    p += 1

    for _ in range(num_arrays):

        header = data[p]
        p += 1

        completeness = header >> 7
        nal_type = header & 0x3F

        num_nalus = struct.unpack(">H", data[p:p+2])[0]
        p += 2

        nal_list = []

        for _ in range(num_nalus):

            length = struct.unpack(">H", data[p:p+2])[0]
            p += 2

            nal = data[p:p+length]
            p += length

            nal_list.append(nal)

        hvcc.arrays.append({
            "type": nal_type,
            "complete": completeness,
            "nalus": nal_list
        })

    return hvcc