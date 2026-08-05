import struct

from parsers.video_tables import get_video_tables

RECOVERED_MOV = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mov\MOV_01m54s_000003.MOV"
)

REBUILT_STSZ = (
    r"C:\Users\johne\OneDrive\Desktop\SonyRecovery"
    r"\rebuilt_stsz.bin"
)


def read_rebuilt_stsz(filename):

    with open(filename, "rb") as f:

        atom_size = struct.unpack(">I", f.read(4))[0]

        atom_type = f.read(4).decode()

        if atom_type != "stsz":
            raise Exception("Not STSZ")

        f.read(4)      # version / flags

        sample_size = struct.unpack(">I", f.read(4))[0]

        if sample_size != 0:
            raise Exception("Unexpected constant sample size")

        sample_count = struct.unpack(">I", f.read(4))[0]

        samples = []

        for _ in range(sample_count):
            samples.append(
                struct.unpack(">I", f.read(4))[0]
            )

    return samples


healthy = get_video_tables(RECOVERED_MOV)["stsz"]
rebuilt = read_rebuilt_stsz(REBUILT_STSZ)

print()
print("=" * 100)
print("STSZ RECONSTRUCTION AUDIT")
print("=" * 100)
print()

print(f"Recovered samples : {len(healthy)}")
print(f"Rebuilt samples   : {len(rebuilt)}")
print(f"Difference        : {len(rebuilt)-len(healthy):+d}")

print()

first_difference = None

for i in range(min(len(healthy), len(rebuilt))):

    if healthy[i] != rebuilt[i]:

        first_difference = i

        print()
        print(f"First difference at sample {i+1:,}")

        print(f"Recovered : {healthy[i]:,}")
        print(f"Rebuilt   : {rebuilt[i]:,}")

        break

if first_difference is None:

    print()
    print("First", len(healthy), "samples are IDENTICAL.")

if len(rebuilt) > len(healthy):

    print()
    print("=" * 60)
    print("EXTRA REBUILT SAMPLES")
    print("=" * 60)

    start = len(healthy)

    print(f"Start sample : {start+1:,}")

    print(f"Extra samples: {len(rebuilt)-len(healthy)}")

    print()

    for i in range(start, min(start+20, len(rebuilt))):

        print(
            f"{i+1:6d} : {rebuilt[i]:,}"
        )

print()

print("=" * 100)
print("DONE")
print("=" * 100)