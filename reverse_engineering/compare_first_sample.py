from repair.recovery_engine import RecoveryEngine

engine = RecoveryEngine()

engine.load_mov(
    r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mov\MOV_01m54s_000003.MOV"
)

frame = engine.frame_map[0]

print()
print("=" * 60)
print("FRAME 1")
print("=" * 60)

print("Offset :", frame["offset"])
print("Size   :", frame["size"])

with open(
    r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mov\MOV_01m54s_000003.MOV",
    "rb"
) as f:

    f.seek(frame["offset"])

    data = f.read(128)

print()

print("First 64 bytes")

for i in range(0, 64, 16):

    row = data[i:i+16]

    print(
        f"{i:04X}  " +
        " ".join(f"{b:02X}" for b in row)
    )

print()

nal_length = int.from_bytes(
    data[:4],
    "big"
)

print("First NAL length:", nal_length)

header = data[4]

print("NAL header byte :", hex(header))

print("NAL type        :", (header >> 1) & 0x3F)