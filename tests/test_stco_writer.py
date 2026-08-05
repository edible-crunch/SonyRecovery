from repair.recovery_engine import RecoveryEngine
from repair.stco_patcher import patch_stco
from repair.stco_writer import write_stco

engine = RecoveryEngine()

engine.load_mov(
    r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mov\MOV_01m54s_000003.MOV"
)

offsets = patch_stco(engine.frame_map)

write_stco(
    "moov.bin",
    "patched_moov.bin",
    engine.tables["stco_atom_offset"],
    offsets
)