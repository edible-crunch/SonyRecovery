from repair.recovery_engine import RecoveryEngine

RECOVERED_MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

RECOVERED_MOV = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mov\MOV_01m54s_000003.MOV"

engine = RecoveryEngine()
engine.load_mov(RECOVERED_MOV)

frame = engine.frame_map[0]

sample_offset = frame["offset"]
sample_size = frame["size"]

print()
print("=" * 70)
print("FRAME 1")
print("=" * 70)
print("Offset :", sample_offset)
print("Size   :", sample_size)

with open(RECOVERED_MP4, "rb") as f:

    f.seek(sample_offset)

    sample = f.read(sample_size)

print("Bytes read :", len(sample))
print()

pos = 0
nal = 1

while pos + 4 <= len(sample):

    print("=" * 60)
    print(f"NAL {nal}")
    print("=" * 60)

    print(f"Sample Offset : {pos:,}")

    print()
    print("Next 32 bytes:")

    blob = sample[pos:pos+32]

    for i in range(0, len(blob), 16):

        row = blob[i:i+16]

        print(
            f"{pos+i:08X}  "
            + " ".join(f"{b:02X}" for b in row)
        )

    print()

    length = int.from_bytes(
        sample[pos:pos+4],
        "big"
    )

    print("Parsed Length :", length)

    if length == 0:

        print("ZERO LENGTH")
        break

    if pos + 4 + length > len(sample):

        print("EXCEEDS SAMPLE")
        break

    header = sample[pos + 4]

    forbidden = (header >> 7) & 1
    nal_type = (header >> 1) & 0x3F

    print("Forbidden Bit :", forbidden)
    print("NAL Type      :", nal_type)

    pos += 4 + length
    nal += 1

    if nal > 5:
        break

print()
print("=" * 70)
print("Finished")
print("=" * 70)