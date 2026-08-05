from repair.hvcc import parse_hvcc
from parsers.mdat_reader import locate_mdat

from recovery.record_stream import RecordStream


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

for array in cfg.arrays:

    if array["type"] == 32:

        vps = array["nalus"][0]
        break

if vps is None:

    raise Exception("No VPS found.")

vps_offset = find_first(payload, vps)

if vps_offset == -1:

    raise Exception("VPS not found.")

record_start = vps_offset - 8

print()
print("VPS Payload Offset :", vps_offset)
print("First Record Offset:", record_start)

stream = RecordStream(payload)

stream.walk(
    record_start,
    max_records=20
)