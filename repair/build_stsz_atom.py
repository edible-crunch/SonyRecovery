import struct

INPUT = "rebuilt_stsz.txt"
OUTPUT = "rebuilt_stsz.bin"

with open(INPUT) as f:
    sizes = [int(x.strip()) for x in f if x.strip()]

sample_count = len(sizes)

payload = bytearray()

# version + flags
payload += b"\x00\x00\x00\x00"

# default sample size (0 = variable)
payload += struct.pack(">I", 0)

# sample count
payload += struct.pack(">I", sample_count)

# sample sizes
for s in sizes:
    payload += struct.pack(">I", s)

atom_size = len(payload) + 8

with open(OUTPUT, "wb") as f:
    f.write(struct.pack(">I", atom_size))
    f.write(b"stsz")
    f.write(payload)

print("=" * 60)
print("STSZ BUILT")
print("=" * 60)
print("Frames:", sample_count)
print("Atom size:", atom_size)
print("Written:", OUTPUT)