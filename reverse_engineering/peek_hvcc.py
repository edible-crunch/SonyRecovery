with open("hvcc.bin", "rb") as f:
    data = f.read(32)

print("Length:", len(data))

print()

for i, b in enumerate(data):
    print(f"{i:02d}: {b:02X}")