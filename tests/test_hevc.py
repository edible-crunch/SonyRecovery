from repair.hevc import parse_header

tests = [
    bytes([0x46,0x01]),
    bytes([0x4E,0x01]),
    bytes([0x40,0x01]),
    bytes([0x42,0x01]),
    bytes([0x44,0x01])
]

for t in tests:

    print(parse_header(t))