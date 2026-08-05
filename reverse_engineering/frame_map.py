from repair.recovery_engine import RecoveryEngine

engine = RecoveryEngine()

engine.load_mov(
    r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mov\MOV_01m54s_000003.MOV"
)

print(engine.frame_map[0])

print(engine.frame_map[1])

print(engine.frame_map[59])

print(engine.frame_map[60])