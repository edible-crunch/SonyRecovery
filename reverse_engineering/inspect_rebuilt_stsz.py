import struct

STSZ = r"C:\Users\johne\OneDrive\Desktop\SonyRecovery\rebuilt_stsz.bin"

sizes = []

with open(STSZ, "rb") as f:

    while True:

        data = f.read(4)

        if len(data) != 4:
            break

        sizes.append(struct.unpack(">I", data)[0])

print("=" * 80)
print("REBUILT STSZ INSPECTOR")
print("=" * 80)

print()
print(f"Total entries : {len(sizes)}")

print()
print("First 20 entries:")

for i, s in enumerate(sizes[:20]):
    print(f"{i+1:02d}: {s:,}")

print()

if len(sizes) >= 60:
    first60 = sum(sizes[:60])

    print(f"Sum of first 60 samples : {first60:,}")

    print(f"Average sample size     : {first60/60:,.1f}")

print()

print("Largest sample :", max(sizes))
print("Smallest sample:", min(sizes))

print()

print("Last 20 entries:")

for i, s in enumerate(sizes[-20:], start=len(sizes)-19):
    print(f"{i:04d}: {s:,}")