from repair.hvcc import parse_hvcc
from parsers.mdat_reader import locate_mdat

from analysis.record_gap import inspect_gap


def find_first(data, pattern):

    return data.find(pattern)


mp4 = input("MP4:\n").strip('"')

hvcc = input("HVCC:\n").strip('"')

mdat = locate_mdat(mp4)

cfg = parse_hvcc(hvcc)

with open(mp4, "rb") as f:

    f.seek(mdat.data_offset)

    payload = f.read(mdat.size)

vps = None
sps = None

for array in cfg.arrays:

    if array["type"] == 32:
        vps = array["nalus"][0]

    if array["type"] == 33:
        sps = array["nalus"][0]

vps_payload = find_first(payload, vps)
sps_payload = find_first(payload, sps)

if vps_payload == -1:
    raise Exception("VPS not found")

if sps_payload == -1:
    raise Exception("SPS not found")

vps_record = vps_payload - 8
sps_record = sps_payload - 8

inspect_gap(
    payload,
    vps_record,
    len(vps),
    sps_record
)