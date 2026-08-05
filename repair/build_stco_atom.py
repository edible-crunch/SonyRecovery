import struct

from repair.stco_generator import generate_stco

RECOVERED_MP4 = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000003.MP4"
)

OUTPUT = "rebuilt_stco.bin"

# ---------------------------------------------------------

offsets = generate_stco(RECOVERED_MP4)

print()
print("=" * 60)
print("BUILDING STCO")
print("=" * 60)

print("Entries :", len(offsets))

# ---------------------------------------------------------
# Build payload
# ---------------------------------------------------------

payload = bytearray()

# version / flags
payload += b"\x00\x00\x00\x00"

# entry count
payload += struct.pack(">I", len(offsets))

# offsets
for offset in offsets:
    payload += struct.pack(">I", offset)

# ---------------------------------------------------------
# Wrap atom
# ---------------------------------------------------------

atom = bytearray()

atom += struct.pack(">I", len(payload) + 8)
atom += b"stco"
atom += payload

# ---------------------------------------------------------

with open(OUTPUT, "wb") as f:
    f.write(atom)

print()
print("[OK] Written")
print(OUTPUT)

print()
print("Atom size :", len(atom))