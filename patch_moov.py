from parsers.video_tables import get_video_tables
from repair.moov_editor import MoovEditor
from repair.stco_writer import write_stco
from repair.stco_rebase import rebase_offsets

# ---------------------------------------------------------

RECOVERED_MOV = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mov\MOV_01m54s_000003.MOV"
)

MOOV_BIN = "moov.bin"

PATCHED_MOOV = "patched_moov.bin"

REBUILT_STSZ = "rebuilt_stsz.bin"

# Leave this as it currently is for this test.
MDAT_DELTA = -44254

# ---------------------------------------------------------

tables = get_video_tables(RECOVERED_MOV)

print()
print("=" * 60)
print("PATCHING MOOV")
print("=" * 60)

# ---------------------------------------------------------
# Load rebuilt STSZ
# ---------------------------------------------------------

with open(REBUILT_STSZ, "rb") as f:
    rebuilt_stsz = f.read()

# ---------------------------------------------------------
# Open editor
# ---------------------------------------------------------

editor = MoovEditor(MOOV_BIN)

# ---------------------------------------------------------
# Replace STSZ
# ---------------------------------------------------------

delta = editor.replace_atom(
    tables["stsz_atom_offset"],
    rebuilt_stsz
)

# ---------------------------------------------------------
# Grow parent atoms
# ---------------------------------------------------------

editor.patch_sizes(
    [
        0,      # moov
        116,    # video trak
        252,    # mdia
        344,    # minf
        408     # stbl
    ],
    delta
)

# ---------------------------------------------------------
# Save intermediate
# ---------------------------------------------------------

editor.save(PATCHED_MOOV)

# ---------------------------------------------------------
# Load VERIFIED chunk starts
# ---------------------------------------------------------

chunk_starts = []

with open("chunk_starts.txt", "r") as f:

    for line in f:

        line = line.strip()

        if line:

            chunk_starts.append(int(line))

print()
print(f"Loaded {len(chunk_starts)} verified chunk starts.")

# ---------------------------------------------------------
# Rebase verified chunk starts
# ---------------------------------------------------------

new_offsets = rebase_offsets(
    chunk_starts,
    MDAT_DELTA
)

# ---------------------------------------------------------
# Patch STCO
# ---------------------------------------------------------

write_stco(
    PATCHED_MOOV,
    PATCHED_MOOV,
    tables["stco_atom_offset"] + delta,
    new_offsets
)

print()
print("=" * 60)
print("DONE")
print("=" * 60)

print()

print(f"STSZ delta : {delta:+,}")

print(f"STCO entries : {len(new_offsets)}")

print("[OK] patched_moov.bin written")